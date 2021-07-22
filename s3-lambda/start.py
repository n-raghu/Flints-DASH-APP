import sys
from zipfile import ZipFile
from iogen import StrIOGenerator

from smart_open import smart_open
from bson.objectid import ObjectId

from essentials import s3_client, s3_rsc

BUCKET = f'boto-ops-s3-{str(ObjectId())}'
BUCKET = 'boto-ops-s3-369'
FZIP = 'datum-lite.zip'
file_ = 'datum/data8216.csv'
file_lite = 'datum/dimYear8277.csv'

# List S3 Buckets
def get_s3_buckets(client=s3_client):
    res = client.list_buckets()
    return res['Buckets']

# Print Bucket Info
def print_bucket_info(bkt=BUCKET, client=s3_client):
    return bkt

# Create S3 Bucket
def create_s3_bucket(bkt=BUCKET, client=s3_client):
    print(bkt)
    return client.create_bucket(
        Bucket=bkt,
        CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
    )

# Push objects to S3
def push_object(bfile, bkt=BUCKET, client=s3_client):
    with open(bfile, 'rb') as bfl:
        bin_data = bfl.read()
    return client.put_object(
        Body=bin_data,
        Bucket=bkt,
        Key=bfile
    )


# Stream Zip to get contents
def zip_stream(zip_f='datum-lite.zip', bkt=BUCKET, client=s3_client):
    s3_uri = f's3://{bkt}/{zip_f}'
    with smart_open(s3_uri, 'rb') as sfile:
        zippo = ZipFile(sfile)
        with zippo.open('data8216', 'r') as dat:
            csv_dat = StrIOGenerator(
                binary_chunk=dat
            )
        print(csv_dat)

# Stream Zip to get contents
def gen_stream(zip_f='datum-lite.zip', bkt=BUCKET, client=s3_client):
    s3_uri = f's3://{bkt}/{zip_f}'
    with smart_open(s3_uri, 'rb') as sfile:
        zippo = ZipFile(sfile)
        with zippo.open('data8216', 'r') as dat:
            for row in csv.DictReader(dat, skipinitialspace=True, delimiter='|'):
                yield {k:v for k,v in row.item()}
