import boto3
from botocore.exceptions import BotoCoreError, ClientError

def read_messages_from_sqs(queue_url, max_messages=10, wait_time=5, visibility_timeout=30):
    """
    Reads messages from an AWS SQS queue.

    :param queue_url: The full URL of the SQS queue.
    :param max_messages: Max number of messages to retrieve (1–10).
    :param wait_time: Long polling wait time in seconds (0–20).
    :param visibility_timeout: Time in seconds the message is hidden after being read.
    """
    # Create SQS client
    sqs = boto3.client("sqs")

    try:
        # Receive messages
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time,
            VisibilityTimeout=visibility_timeout,
            AttributeNames=["All"]
        )

        attributes = response.get("Attributes", {})
        print("Queue Attributes:")
        for key, value in attributes.items():
            print(f"  {key}: {value}")

        messages = response.get("Messages", [])
        if not messages:
            print("No messages available in the queue.")
            return
        
        for msg in messages:
            print(f"Message ID: {msg['MessageId']}")
            print(f"Body: {msg['Body']}")
            print("-" * 40)
            ''''''
            # Process the message here
            # Example: store in DB, trigger workflow, etc.
            # Delete message after successful processing
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg["ReceiptHandle"]
            )
            print(f"Deleted message {msg['MessageId']} from queue.")
    except (BotoCoreError, ClientError) as e:
        print(f"Error reading from SQS: {e}")

if __name__ == "__main__":
    # Replace with your actual SQS queue URL
    QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/216990846240/caleb-queue"

    read_messages_from_sqs(
        queue_url=QUEUE_URL,
        max_messages=5,
        wait_time=10,
        visibility_timeout=30
    )
