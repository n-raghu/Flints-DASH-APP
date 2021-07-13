import yaml
from boto3 import resource as botorsc
from boto3 import client as botoclient


with open('../credentials.yml', 'r') as cfile:
    cfg = yaml.safe_load(cfile)

aws_region = cfg['aws_region']
aws_key = cfg['aws_key']
aws_access = cfg['aws_access']
departments: list = ['dev', 'test', 'srt']

# Create Client for DynamoDB
dynamo_client = botoclient(
    'dynamodb',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_access,
    region_name=aws_region
)

# Create Resource for DynamoDB
dynamo_rsc = botorsc(
    'dynamodb',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_access,
    region_name=aws_region
)

# Create Client for S3
s3_client = botoclient(
    's3',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_access,
    region_name=aws_region
)

# Create Resource for S3
s3_rsc = botorsc(
    's3',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_access,
    region_name=aws_region
)
