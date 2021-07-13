# DynamoDB
<p>NoSQL database offered by Amazon</p>

## gen_db.py

### About
File to generate random data and push to dynamoDB.

### Functions
#### create_tab
**Purpose**: Create a table on DynamoDB
**Accepts**: 2 arguments
1. _tbl_ -> name of table to be created
2. _client__ -> active amazon client session to connect and create table
**Returns**: None

#### gen_usr
**Purpose**: Generate a random user
**Accepts**: 3 arguments
1. _dep_ -> Dept Name
2. _tbl_ -> Table Name
3. _sal_r_ -> Salary Range
**Returns**: A dictionary with user props

#### create_users
**Purpose**: Prepare a dictionary in the format required by batch writer using input dict. Dictionary will hold list of user items
**Accepts**: 2 arguments
1. _db_items_ -> Dictionary of user items with table name
3. _client_ -> Activated boto3 client
**Returns**: None

#### create_116_set
**Purpose**: Generate chunks of users using `gen_user`, each chunk will have 20 users. Now push each chunk to DynamoDB using `create_users`
**Accepts**: 3 arguments
1. _tname_ -> Table Name
2. _client__ -> Activated boto3 client
3. _deps_ -> List of departments
**Returns**: None

#### create_116_set
**Purpose**: Orchestrate the entire process and test with default values
**Accepts**: 1 argument
1. _client__ -> Activated boto3 client
**Returns**: None


## qry_db.py
File with queries for existing DynamoDB

#### Concepts
`get_item` retrieve via hash and range key is a 1:1 fit, the time it takes (hence performance) to retrieve it is limited by the hash and sharding internally.
(From the docs)
**GetItem** – Retrieves a single item from a table.
This is the most efficient way to read a single item because it provides direct access to the physical location of the item. 
(DynamoDB also provides the BatchGetItem operation, allowing you to perform up to 100 GetItem calls in a single operation.)

`query` results in a search on "all" range keys. It adds computational work, thus considered slower
(From the docs)
**Query** – Retrieves all of the items that have a specific partition key.
Within those items, you can apply a condition to the sort key and retrieve only a subset of the data.
Query provides quick, efficient access to the partitions where the data is stored.

`ExecuteStatement` – Retrieves a single or multiple items from a table using the PartiQL (a SQL compatible query language).
DynamoDB also provides the BatchExecuteStatement operation, allowing you to retrieve multiple items from diffrent tables in a single operation.

`Scan` – Retrieves all of the items in the specified table.
(This operation should not be used with large tables because it can consume large amounts of system resources.)
