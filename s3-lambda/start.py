import sys

from bson.objectid import ObjectId

from zipops import get_zip_file
from essentials import s3_client, s3_rsc

BUCKET = f'boto-ops-s3-{str(ObjectId())}'
csv_file = 'datum/dim_users.csv'

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

# List objects from S3

# Read S3 objects
files = get_zip_file('boto-ops-s3-369', 'datum.zip')

# Delete S3 bucket
def drop_bucket(bkt=BUCKET, client=s3_client):
    return bkt
