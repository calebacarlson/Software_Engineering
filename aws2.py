import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def list_s3_objects(bucket_name, prefix=""):
    """
    List all objects in an S3 bucket.
    
    :param bucket_name: Name of the S3 bucket
    :param prefix: Optional prefix to filter objects (like a folder path)
    """
    try:
        # Create S3 client
        s3_client = boto3.client("s3")

        # Use paginator for large buckets
        paginator = s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        object_count = 0
        for page in page_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    print(obj["Key"])
                    object_count += 1

        if object_count == 0:
            print("No objects found in the bucket.")

    except NoCredentialsError:
        print("AWS credentials not found. Please configure them using AWS CLI or environment variables.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials. Please check your configuration.")
    except ClientError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace with your bucket name
    bucket_name = "bucket-software-engineering"
    list_s3_objects(bucket_name)