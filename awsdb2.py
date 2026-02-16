import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# ---------- CONFIGURATION ----------
TABLE_NAME = "YourTableName"  # Replace with your DynamoDB table name
REGION_NAME = "us-east-1"     # Replace with your AWS region

# Create DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name=REGION_NAME)

def add_item(item_data):
    """
    Adds a single item to the DynamoDB table.
    :param item_data: dict containing the item attributes
    """
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.put_item(Item=item_data)
        print(f"✅ Item added successfully: {item_data}")
        return response
    except (NoCredentialsError, PartialCredentialsError):
        print("❌ AWS credentials not found or incomplete. Configure them with `aws configure`.")
    except ClientError as e:
        print(f"❌ Failed to add item: {e.response['Error']['Message']}")


if __name__ == "__main__":
    # Example: Add a single item
    single_item = {
        "year": "2019",       # Partition key
        "title": "Tall Girl"      # Sort key (if your table has one)
    }
    add_item(single_item)
