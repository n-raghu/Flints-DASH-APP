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