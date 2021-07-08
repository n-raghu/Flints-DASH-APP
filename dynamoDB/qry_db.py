from boto3.dynamodb.conditions import Key, Attr

from essentials import dynamo_client, dynamo_rsc, departments

"""
`get_item` retrieve via hash and range key is a 1:1 fit, the time it takes (hence performance) to retrieve it is limited by the hash and sharding internally.
`query` results in a search on "all" range keys. It adds computational work, thus considered slower

From the docs:
ExecuteStatement – Retrieves a single or multiple items from a table using the PartiQL (a SQL compatible query language).
DynamoDB also provides the BatchExecuteStatement operation, allowing you to retrieve multiple items from diffrent tables in a single operation.

GetItem – Retrieves a single item from a table.
This is the most efficient way to read a single item because it provides direct access to the physical location of the item. 
(DynamoDB also provides the BatchGetItem operation, allowing you to perform up to 100 GetItem calls in a single operation.)

Query – Retrieves all of the items that have a specific partition key.
Within those items, you can apply a condition to the sort key and retrieve only a subset of the data.
Query provides quick, efficient access to the partitions where the data is stored.

Scan – Retrieves all of the items in the specified table.
(This operation should not be used with large tables because it can consume large amounts of system resources.)
"""

# Get count, creation time of collection, only refreshes once in 6hrs
def tab_props(tbl: str='usrsalary', rsc_=dynamo_rsc):
    collection = rsc_.Table(tbl)
    return {
        'count': collection.item_count,
        'created_at': collection.creation_date_time
    }

# Retrieve a single item from DynamoDB
def simple_get_item(dep: str, tbl: str='usrsalary', rsc_=dynamo_rsc):
    collection = rsc_.Table(tbl)
    response = collection.get_item(Key={'dep': dep, 'salary': 300})
    return response['Item']

# query a collection
def simple_query_tab(dep: str, tbl: str='usrsalary', rsc_=dynamo_rsc):
    collection = rsc_.Table(tbl)
    response = collection.query(
        KeyConditionExpression=Key('dep').eq(f'{dep}'))
    return response['Items']

# Scan a collection
def simple_scan_tab(sal: int, tbl: str='usrsalary', rsc_=dynamo_rsc):
    collection = rsc_.Table(tbl)
    response = collection.scan(
        FilterExpression=Attr('salary').lte(sal)
    )
    return response['Items']

# Multiple scan conditions
def scan_tab(dep, sal1, sal2, tbl: str='usrsalary', rsc_=dynamo_rsc):
    collection = rsc_.Table(tbl)
    response = collection.scan(
        FilterExpression=Attr('salary').gte(sal1) &
        Attr('salary').lte(sal2) &
        Attr('dep').eq('dev')
    )
    return response['Items']


if __name__ == '__main__':
    item = scan_tab('dev', 3600, 6900)
    print(item)
