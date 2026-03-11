'''
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def list_dynamodb_tables(region="us-east-1"):
    # Create DynamoDB client
    dynamodb = boto3.client("dynamodb", region_name=region)

    tables = []
    last_evaluated_table = None

    while True:
        if last_evaluated_table:
            response = dynamodb.list_tables(ExclusiveStartTableName=last_evaluated_table)
        else:
            response = dynamodb.list_tables()

        tables.extend(response.get("TableNames", []))
        last_evaluated_table = response.get("LastEvaluatedTableName")

        if not last_evaluated_table:
            break

    return tables




if __name__ == "__main__":
    all_tables = list_dynamodb_tables()
    print("DynamoDB Tables:", all_tables)
'''

import math

import boto3
from botocore.exceptions import BotoCoreError, ClientError

def list_all_items(table_name, region="us-east-1"):
    """
    Lists all items from a DynamoDB table.
    Handles pagination to retrieve more than 1MB of data.
    """
    try:
        # Create DynamoDB resource
        dynamodb = boto3.resource("dynamodb", region_name=region)
        table = dynamodb.Table(table_name)

        items = []
        response = table.scan()
        items.extend(response.get("Items", []))

        # Keep scanning if there are more items
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response.get("Items", []))

        return items

    except (BotoCoreError, ClientError) as e:
        print(f"Error fetching items: {e}")
        return []
    
def mean(list):
    numberOfItems = len(list)
    sum = 0
    for i in list:
        sum += i
    return sum / numberOfItems

def median(list):
    numberOfItems = len(list)
    list.sort()
    if (numberOfItems % 2) == 0:
        # even
        return mean(list = [list[numberOfItems-math.floor(numberOfItems/2)-1], list[numberOfItems-math.floor(numberOfItems/2)]])
    else:
        #odd
        return list[numberOfItems-math.floor(numberOfItems/2)-1]
    
def stddev(list):
    numberOfItems = len(list)
    mean_ = mean(list)
    sum = 0
    for i in list:
        sum += math.pow(i-mean_, 2)

    
    return math.sqrt(sum/numberOfItems)


if __name__ == "__main__":
    '''
    table_name = "CIS3823Spring26"  # Replace with your DynamoDB table name
    all_items = list_all_items(table_name)

    print(f"Total items retrieved: {len(all_items)}")
    for item in all_items:
        print(item.get('task'))
    '''

    print(mean(list = [1, 2, 3, 10, 14, 6, 7]))
    print(median(list = [1, 2, 3, 10, 14, 6, 7]))
    print(stddev(list = [1, 2, 3, 10, 14, 6, 7]))