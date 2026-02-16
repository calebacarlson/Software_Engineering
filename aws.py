import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def list_s3_buckets():
    try:
        # Create an S3 client using default AWS credentials/config
        s3 = boto3.client('s3')

        # Retrieve the list of buckets
        response = s3.list_buckets()

        # Check if buckets exist
        if 'Buckets' in response and response['Buckets']:
            print("S3 Buckets in your account:")
            for bucket in response['Buckets']:
                print(f" - {bucket['Name']}")
        else:
            print("No S3 buckets found in your account.")

    except NoCredentialsError:
        print("Error: AWS credentials not found. Configure them using 'aws configure'.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials. Please check your AWS configuration.")
    except ClientError as e:
        print(f"AWS Client Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    list_s3_buckets()