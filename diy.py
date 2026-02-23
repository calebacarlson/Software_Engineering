import boto3
import botocore
import sys

def read_numbers_from_s3(bucket, key):
    """Read a list of numbers from a text file in S3."""
    s3 = boto3.client("s3", region_name="us-east-1")
    obj = s3.get_object(Bucket=bucket, Key=key)
    content = obj["Body"].read().decode("utf-8")
    print(content)

bucket = "exam-prep-statistics-bucket"
key = "sample.txt"

read_numbers_from_s3(bucket, key)


