import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def send_sqs_message(message_body, message_group_id=None, queue_url= "https://sqs.us-east-1.amazonaws.com/216990846240/caleb-queue"):

    # Create SQS client
    sqs = boto3.client("sqs")

    # Prepare parameters
    params = {
        "QueueUrl": queue_url,
        "MessageBody": message_body
    }

    # FIFO queues require MessageGroupId
    if ".fifo" in queue_url:
        if not message_group_id:
            raise ValueError("FIFO queues require a message_group_id.")
        params["MessageGroupId"] = message_group_id

    # Send the message
    response = sqs.send_message(**params)
    print(f"Message sent successfully! MessageId: {response['MessageId']}")
    return response["MessageId"]




if __name__ == "__main__":
    # Example usage
    # Replace with your actual SQS queue URL
    queue_url = "https://sqs.us-east-1.amazonaws.com/216990846240/caleb-queue"
    message_body = "Hello from Python!"
    
    # For FIFO queues, provide a group ID
    message_group_id = "group1"  # Only needed if queue_url ends with .fifo

    send_sqs_message(queue_url, message_body, message_group_id)
