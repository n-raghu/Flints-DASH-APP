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
2. _client_ -> active amazon client session to connect and create table
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
2. _client_ -> Activated boto3 client
3. _deps_ -> List of departments
**Returns**: None

#### create_116_set
**Purpose**: Orchestrate the entire process and test with default values
**Accepts**: 1 argument
1. _client__ -> Activated boto3 client
**Returns**: None
