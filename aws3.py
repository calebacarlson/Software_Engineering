import boto3
from botocore.exceptions import ClientError
import sys
import re

def create_s3_bucket(bucket_name, region=None):
    """
    Create an S3 bucket in a specified region.
    If no region is specified, the bucket is created in the default region (us-east-1).
    """
    # Validate bucket name according to AWS rules
    if not re.match(r'^[a-z0-9.-]{3,63}$', bucket_name):
        raise ValueError("Invalid bucket name. Must be 3-63 characters, lowercase letters, numbers, dots, or hyphens.")

    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

        print(f"✅ Bucket '{bucket_name}' created successfully in region: {region or 'us-east-1'}")

    except ClientError as e:
        print(f"❌ Error creating bucket: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage
    bucket_name = "my-unique-bucket-name-12345"  # Must be globally unique
    region = "us-west-2"  # Change as needed, or set to None for default

    try:
        create_s3_bucket(bucket_name, region)
    except ValueError as ve:
        print(f"❌ Validation error: {ve}")