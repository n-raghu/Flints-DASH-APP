def query_table(tbl, rsc_):
    collection = rsc_.Table(tbl)
    response = collection.query(
        KeyConditionExpression=Key('salary').lte('9000')
    )
    return response


