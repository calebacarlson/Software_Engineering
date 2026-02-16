import boto3
from botocore.exceptions import BotoCoreError, ClientError

def list_dynamodb_values(table_name, attribute_name=None):
    """
    Lists all items in a DynamoDB table and optionally extracts values for a specific attribute.
    
    :param table_name: Name of the DynamoDB table
    :param attribute_name: Optional attribute to extract values from
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    try:
        # Scan the table (fetch all items)
        response = table.scan()
        items = response.get("Items", [])

        # Handle pagination if table has more than 1MB of data
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response.get("Items", []))

        if attribute_name:
            # Extract only the requested attribute values
            values = [item.get(attribute_name) for item in items if attribute_name in item]
            print(f"Values for '{attribute_name}': {values}")
            return values
        else:
            print("All items in table:")
            for item in items:
                print(item)
            return items

    except (BotoCoreError, ClientError) as e:
        print(f"Error fetching data from DynamoDB: {e}")
        return []

# Example usage:
# List all items
list_dynamodb_values("Movies")