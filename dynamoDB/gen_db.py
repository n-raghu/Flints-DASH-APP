import sys
import math
from uuid import uuid1 as UU1
from random import choice, shuffle
from datetime import datetime as dtm

import yaml
from bson.objectid import ObjectId
from boto3 import resource as botorsc
from boto3 import client as botoclient
from boto3.dynamodb.conditions import Key

with open('../credentials.yml', 'r') as cfile:
    cfg = yaml.safe_load(cfile)

aws_region = cfg['aws_region']
aws_key = cfg['aws_key']
aws_access = cfg['aws_access']
departments: list = ['dev', 'test', 'srt']
sal_range = list(range(100, 100000, 100))
shuffle(sal_range)

# Create Client for Session
amazonclient = botoclient(
    'dynamodb',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_access,
    region_name=aws_region
)


# Create Table
def create_tab(tbl, client_):
    return client_.create_table(
        TableName=tbl,
        AttributeDefinitions=[
            {
                "AttributeName": "dep",
                "AttributeType": "S"
            },
            {
                "AttributeName": "salary",
                "AttributeType": "N"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "dep",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "salary",
                "KeyType": "RANGE"
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )


# Function to Generate Record
def gen_usr(dep, tbl, sal_r=sal_range):
    uid = str(ObjectId())
    document_id = UU1().hex
    try:
        usal = sal_r.pop()
    except Exception as err:
        sys.exit(err)
    return {
        'created_stamp': {'S': dtm.utcnow().isoformat()},
        'uid': {'S': uid},
        'dep': {'S': dep},
        'document_id': {'S': document_id},
        'active': {'BOOL': True},
        'salary': {'N': str(usal)}
    }


# Create user on dynamoDB
def create_usr(db_items, client):
    push_items: dict = {}
    for col_, items_ in db_items.items():
        collection_items: list = []
        for item in items_:
            collection_items.append(
                {
                    'PutRequest': {'Item': item}
                }
            )
        push_items[col_] = collection_items

    return client.batch_write_item(
        RequestItems=push_items,
        ReturnConsumedCapacity='TOTAL',
        ReturnItemCollectionMetrics='SIZE'
    )


# Create 100 test sets
def create_100_set(tname, client_, deps=departments):
    usr_items = []
    csize = 20
    for _ii in range(116):
        usr_items.append(gen_usr(choice(deps), tname))
    chunks = math.ceil(len(usr_items)/csize)
    for n in range(chunks):
        create_usr({tname: usr_items[n*csize:(n+1)*csize]}, client_)
        print(n)


def tester(client_ = amazonclient):
    tb_ = 'usrsalary'
    try:
        create_tab(tb_, client_)
    except Exception:
        print('Table seems exists!!!')

    create_100_set(tb_, client_,)


def query_table(tbl, rsc_):
    collection = rsc_.Table(tbl)
    response = collection.query(
        KeyConditionExpression=Key('salary').lte('9000')
    )
    return response


tab_rsc = botorsc(
    'dynamodb',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_access,
    region_name=aws_region
)


if __name__ == '__main__':
    tester()
