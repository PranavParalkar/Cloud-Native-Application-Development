import boto3 
  
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
  
table = dynamodb.create_table( 
    TableName='Students', 
    KeySchema=[ 
        {'AttributeName': 'student_id', 'KeyType': 'HASH'},   # Partition key 
        {'AttributeName': 'name',       'KeyType': 'RANGE'},  # Sort key 
    ], 
    AttributeDefinitions=[ 
        {'AttributeName': 'student_id', 'AttributeType': 'S'}, 
        {'AttributeName': 'name',       'AttributeType': 'S'}, 
    ], 
    BillingMode='PAY_PER_REQUEST'  # On-demand pricing 
) 
table.wait_until_exists() 
print('Table created:', table.table_name) 

table = dynamodb.Table('Students') 
  
# Insert a single item 
table.put_item(Item={ 
    'student_id': 'S001', 
    'name': 'Alice Johnson', 
    'age': 22, 
    'grade': 'A', 
    'courses': ['AWS', 'Python', 'DevOps'] 
}) 
print('Item inserted.') 
  
# Batch write multiple items 
with table.batch_writer() as batch: 
    batch.put_item(Item={'student_id': 'S002', 'name': 'Bob Smith', 'age': 23, 
'grade': 'B'}) 
    batch.put_item(Item={'student_id': 'S003', 'name': 'Carol White', 'age': 21, 
'grade': 'A'}) 
print('Batch insert complete.')

# Get a single item by primary key 
response = table.get_item( 
    Key={'student_id': 'S001', 'name': 'Alice Johnson'} 
) 
item = response.get('Item') 
if item: 
    print('Found:', item) 
else: 
    print('Item not found.')

from boto3.dynamodb.conditions import Attr 
  
# Scan entire table 
response = table.scan() 
for item in response['Items']: 
    print(item) 
  
# Scan with filter 
response = table.scan( 
    FilterExpression=Attr('grade').eq('A') 
) 
print('Grade-A students:', len(response['Items']))

from boto3.dynamodb.conditions import Key 
  
response = table.query( 
    KeyConditionExpression=Key('student_id').eq('S001') 
) 
for item in response['Items']: 
    print(item)

table.update_item( 
    Key={'student_id': 'S001', 'name': 'Alice Johnson'}, 
    UpdateExpression='SET grade = :g, age = :a', 
    ExpressionAttributeValues={':g': 'A+', ':a': 23}, 
    ReturnValues='UPDATED_NEW' 
) 
print('Item updated.')

table.delete_item( 
Key={'student_id': 'S003', 'name': 'Carol White'} 
) 
print('Item deleted.') 

# table.delete() 
# print('Table deleted.')