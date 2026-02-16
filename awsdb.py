import boto3
from botocore.exceptions import ClientError

def create_dynamodb_table():
    # Create DynamoDB client
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    try:
        # Create table
        table = dynamodb.create_table(
            TableName='Movies',
            KeySchema=[
                {'AttributeName': 'year', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'title', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'year', 'AttributeType': 'N'},  # Number
                {'AttributeName': 'title', 'AttributeType': 'S'}  # String
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        print("Creating table... Please wait.")
        # Wait until the table exists
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName='Movies')

        print(f"Table status: {table['TableDescription']['TableStatus']}")
        print("Table created successfully!")

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists.")
        else:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    create_dynamodb_table()