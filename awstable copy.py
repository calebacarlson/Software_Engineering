import boto3
from botocore.exceptions import BotoCoreError, ClientError
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def read_all_items(table_name, region_name="us-east-1"):

    # Initialize DynamoDB resource
    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    table = dynamodb.Table(table_name)

    items = []
    last_evaluated_key = None

    while True:
        # Prepare scan parameters
        scan_kwargs = {}
        if last_evaluated_key:
            scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

        # Perform scan
        response = table.scan(**scan_kwargs)
        items.extend(response.get("Items", []))

        # Check if there are more items to fetch
        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

    return items



def get_txt_from_s3(bucket_name, file_key, aws_region="us-east-1"):

    # Create S3 client
    s3_client = boto3.client("s3", region_name=aws_region)

    # Get the object
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)

    # Read and decode file content
    content = response["Body"].read().decode("utf-8")
    return content



def put_item_to_dynamodb(table_name, item):

    # Create DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # Get table reference
    table = dynamodb.Table(table_name)

    # Put item into table
    response = table.put_item(Item=item)

    print("Item successfully inserted!")
    print("DynamoDB Response:", response)







# Example usage
if __name__ == "__main__":
    #--------------------------------------------------------
    table_name = "CIS3823Spring26Exams"
    all_items = read_all_items(table_name)

    print(f"Retrieved {len(all_items)} items from '{table_name}'")
    for item in all_items:
        if item.get('student') == 'carlson-caleb':
            print(item)
            my_item = item
    print("this is my item",my_item)

    bucket = my_item.get('s3-bucket')
    print(bucket)

    file = my_item.get('s3-object')
    print(file)

    content = get_txt_from_s3(bucket, file)
    if content:
        print("File content retrieved successfully:\n")
        print(content)

    qanda = content.splitlines() 
    q = qanda[0]

    qanda = content.splitlines() 
    a = qanda[1]

    print("q is:"+q+"\na is:"+a)

    id_key = my_item.get('id')

    item = {
        'id': id_key,
        "answer": a,
        "question": q
    }

    put_item_to_dynamodb(table_name, item)

    '''

    #--------------------------------------------------------
    bucket = "exam-prep-statistics-bucket"
    key = "data/numbers_test_01.txt"

    content = get_txt_from_s3(bucket, key)
    if content:
        print("File content retrieved successfully:\n")
        print(content)

    #--------------------------------------------------------
    # Example item (must match your table's key schema)
    item = {
        "author": "carlson-caleb",       # Partition key
        "answer": "works11"
    }

    put_item_to_dynamodb(table_name, item)
        
        '''
