import io
import sys
#from io import BytesIO
from zipfile import ZipFile

from smart_open import open as sopen
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

# Delete S3 bucket
def drop_bucket(bkt=BUCKET, client=s3_client):
    return bkt

# Stream Zip
def zip_stream(zip_f='datum-lite.zip', bkt=BUCKET, rsc=s3_rsc):
    obj = rsc.Object(
        bucket_name=bkt,
        key=zip_f
    )

    return obj.get()['Body'].read()

    return ZipFile(io.BytesIO(obj.get()['Body'].read()))

def files_in_zip():
    zippo = zip_stream()
    return [csv.filename for csv in zippo.filelist if '.csv' in csv.filename]
