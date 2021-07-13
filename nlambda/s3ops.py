import sys

from bson.objectid import ObjectId

from essentials import s3_client

BUCKET = f'boto-ops-s3-{str(ObjectId())}'
print(BUCKET)

# List S3 Buckets
def get_s3_buckets(client=s3_client):
    res = client.list_buckets()
    return res['Buckets']

# Create S3 Bucket
def create_s3_bucket(bkt=BUCKET, client=s3_client):
    return client.create_bucket(
        Bucket=bkt,
        CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
    )


# Push objects to S3

# Read objects from S3


# Open S3 objects

# Delete S3 bucket
