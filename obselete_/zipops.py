from io import BytesIO
from struct import unpack
from zipfile import ZipFile

import boto3

from essentials import s3_client as s3

EOCD_RECORD_SIZE = 22
ZIP64_EOCD_RECORD_SIZE = 56
ZIP64_EOCD_LOCATOR_SIZE = 20

MAX_STANDARD_ZIP_SIZE = 4_294_967_295


def lambda_handler(bucket, key):
    zip_file = get_zip_file(bucket, key)
    print_zip_content(zip_file)

def get_zip_file(bucket, key):
    file_size = get_file_size(bucket, key)
    eocd_record = fetch(bucket, key, file_size - EOCD_RECORD_SIZE, EOCD_RECORD_SIZE)
    if file_size <= MAX_STANDARD_ZIP_SIZE:
        cd_start, cd_size = get_central_directory_metadata_from_eocd(eocd_record)
        central_directory = fetch(bucket, key, cd_start, cd_size)
        return ZipFile(BytesIO(central_directory + eocd_record))
    else:
        zip64_eocd_record = fetch(bucket, key,
                                  file_size - (EOCD_RECORD_SIZE + ZIP64_EOCD_LOCATOR_SIZE + ZIP64_EOCD_RECORD_SIZE),
                                  ZIP64_EOCD_RECORD_SIZE)
        zip64_eocd_locator = fetch(bucket, key,
                                   file_size - (EOCD_RECORD_SIZE + ZIP64_EOCD_LOCATOR_SIZE),
                                   ZIP64_EOCD_LOCATOR_SIZE)
        cd_start, cd_size = get_central_directory_metadata_from_eocd64(zip64_eocd_record)
        central_directory = fetch(bucket, key, cd_start, cd_size)
        return ZipFile(BytesIO(central_directory + zip64_eocd_record + zip64_eocd_locator + eocd_record))


def get_file_size(bucket, key):
    head_response = s3.head_object(Bucket=bucket, Key=key)
    return head_response['ContentLength']

def fetch(bucket, key, start, length):
    end = start + length - 1
    response = s3.get_object(Bucket=bucket, Key=key, Range="bytes=%d-%d" % (start, end))
    return response['Body'].read()

def get_central_directory_metadata_from_eocd(eocd):
    cd_size = parse_little_endian_to_int(eocd[12:16])
    cd_start = parse_little_endian_to_int(eocd[16:20])
    return cd_start, cd_size

def get_central_directory_metadata_from_eocd64(eocd64):
    cd_size = parse_little_endian_to_int(eocd64[40:48])
    cd_start = parse_little_endian_to_int(eocd64[48:56])
    return cd_start, cd_size

def parse_little_endian_to_int(little_endian_bytes):
    format_character = "i" if len(little_endian_bytes) == 4 else "q"
    return unpack("<" + format_character, little_endian_bytes)[0]

def print_zip_content(zip_file):
    files = [zi.filename for zi in zip_file.filelist]
    print(f"Files: {files}")
