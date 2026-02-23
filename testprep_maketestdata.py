import boto3
import botocore
import uuid
import sys

def create_s3_bucket_with_file(bucket_name_prefix, file_name, file_content, region="us-east-1"):
    """
    Creates an S3 bucket and uploads a text file to it.
    """
    try:
        # Create a unique bucket name (S3 bucket names must be globally unique)
        bucket_name = f"{bucket_name_prefix}-{uuid.uuid4()}"
        
        # Initialize S3 client
        s3_client = boto3.client("s3", region_name=region)
        
        # Create the bucket
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        print(f"✅ Bucket created: {bucket_name}")
        
        # Write content to a local file
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(file_content)
        
        # Upload file to S3
        s3_client.upload_file(file_name, bucket_name, file_name)
        print(f"✅ File '{file_name}' uploaded to bucket '{bucket_name}'")
        
        return bucket_name
    
    except botocore.exceptions.ClientError as e:
        print(f"❌ AWS Client Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage
    bucket_prefix = "my-dynamodb-data"
    file_name = "sample.txt"
    file_content = "1,2,3,4,5,6,7,8,9,10"
    
    create_s3_bucket_with_file(bucket_prefix, file_name, file_content)