import csv
import json
import boto3
import codecs


s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
bucket = 'boto-ops-s3-369'
key = 'data8216.csv'
tableName = 'csvdumps'


def handler(event, context):
    obj = s3.Object(bucket, key).get()['Body']
    table = dynamodb.Table(tableName)
    batch_size = 100
    batch = []
    for row in csv.DictReader(codecs.getreader('utf-8')(obj)):
        if len(batch) >= batch_size:
            write_to_dynamo(batch)
            return {
                'statusCode': 200,
                'body': {
                    "msg": "Completed"
                }
            }
            batch.clear()

        batch.append(row)


def write_to_dynamo(rows):
    table = dynamodb.Table(tableName)

    with table.batch_writer() as batch:
        for i in range(len(rows)):
            batch.put_item(Item=rows[i])
