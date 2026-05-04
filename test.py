import boto3
from botocore.exceptions import BotoCoreError, ClientError

def get_all_items_from_dynamodb(table_name, region_name="us-east-1"):
    """
    Retrieve all items from a DynamoDB table.
    
    Args:
        table_name (str): Name of the DynamoDB table.
        region_name (str): AWS region where the table is hosted.
    
    Returns:
        list: A list of all items in the table.
    
    Raises:
        ValueError: If table_name is empty.
        RuntimeError: If AWS request fails.
    """
    if not table_name or not isinstance(table_name, str):
        raise ValueError("Table name must be a non-empty string.")

    # Create DynamoDB resource
    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    table = dynamodb.Table(table_name)

    items = []
    try:
        # Initial scan
        response = table.scan()
        items.extend(response.get("Items", []))

        # Continue scanning if there are more pages
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response.get("Items", []))

    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to retrieve items from {table_name}: {e}")

    return items


# Example usage:
if __name__ == "__main__":
    try:
        all_items = get_all_items_from_dynamodb("YourTableName", region_name="us-east-1")
        print(f"Retrieved {len(all_items)} items.")
        for item in all_items:
            print(item)
    except Exception as e:
        print(f"Error: {e}")
