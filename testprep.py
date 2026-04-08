import boto3
import botocore
import sys

# ---------- CONFIGURATION ----------
S3_BUCKET = "my-dynamodb-data"
S3_KEY = "path/to/numbers.txt"  # The text file in S3
DYNAMODB_TABLE = "YourDynamoDBTable"
PARTITION_KEY = "id"  # Change to your table's partition key name
AWS_REGION = "us-east-1"
# -----------------------------------

def read_numbers_from_s3(bucket, key):
    """Read a list of numbers from a text file in S3."""
    s3 = boto3.client("s3", region_name=AWS_REGION)
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj["Body"].read().decode("utf-8")
        # Split by whitespace/newlines and filter out empty strings
        numbers = [n.strip() for n in content.split() if n.strip()]
        return numbers
    except botocore.exceptions.ClientError as e:
        print(f"Error reading S3 file: {e}")
        sys.exit(1)

def batch_get_from_dynamodb(table_name, key_name, keys):
    """Retrieve multiple items from DynamoDB using BatchGetItem."""
    dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)

    # DynamoDB BatchGetItem limit: 100 items per request
    results = []
    for i in range(0, len(keys), 100):
        batch_keys = keys[i:i+100]
        request_items = {
            table_name: {
                "Keys": [{key_name: {"N": str(k)}} for k in batch_keys]
            }
        }
        try:
            response = dynamodb.batch_get_item(RequestItems=request_items)
            items = response.get("Responses", {}).get(table_name, [])
            results.extend(items)

            # Handle unprocessed keys (retry)
            while "UnprocessedKeys" in response and response["UnprocessedKeys"]:
                response = dynamodb.batch_get_item(RequestItems=9["UnprocessedKeys"])
                items = response.get("Responses", {}).get(table_name, [])
                results.extend(items)

        except botocore.exceptions.ClientError as e:
            print(f"Error fetching from DynamoDB: {e}")
            sys.exit(1)

    return results

if __name__ == "__main__":
    # Step 1: Read numbers from S3
    numbers = read_numbers_from_s3(S3_BUCKET, S3_KEY)
    print(f"Numbers read from S3: {numbers}")

    # Step 2: Get matching items from DynamoDB
    items = batch_get_from_dynamodb(DYNAMODB_TABLE, PARTITION_KEY, numbers)

    # Step 3: Print results
    print("DynamoDB Items Retrieved:")
    for item in items:
        print(item)
