from boto3.dynamodb.conditions import Key

from essentials import dynamo_client, dynamo_rsc, departments

"""
`get_item` retrieve via hash and range key is a 1:1 fit, the time it takes (hence performance) to retrieve it is limited by the hash and sharding internally.
`query` results in a search on "all" range keys. It adds computational work, thus considered slower
"""

# Retrieve a single item from DynamoDB
def simple_get_item(dep: str, tbl: str='usrsalary', rsc_=dynamo_rsc):
    collection = rsc_.Table(tbl)
    response = collection.get_item(Key={'dep': dep, 'salary': 300})
    return response['Item']

# query a collection
def simple_query_tab(dep: str, tbl: str='usrsalary', rsc_=dynamo_rsc):
    collection = rsc_.Table(tbl)
    response = collection.query(Key={'dep': dep})
    return response['Item']


if __name__ == '__main__':
    item = simple_query_tab('dev')
    print(item)
