import boto3

def receive_message_with_attributes(queue_url, max_messages=1, wait_time=0):

    sqs = boto3.client("sqs")

    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=["All"],  # System attributes
        MessageAttributeNames=["All"],  # Custom attributes
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time
    )

    messages = response.get("Messages", [])
    if not messages:
        print("No messages found in the queue.")
        return
    
    messageList = []

    for idx, msg in enumerate(messages, start=1):
        print(f"\n--- Message {idx} ---")
        print(f"MessageId: {msg.get('MessageId')}")
        print(f"Body: {msg.get('Body')}")
        print(f"System Attributes: {msg.get('Attributes')}")
        print(f"Custom Attributes: {msg.get('MessageAttributes')}")

        messageList.append([idx, msg.get('MessageId'), msg.get('Body'), msg.get('Attributes')], msg.get('MessageAttributes'))

        # If you don't want to delete the message, skip this step
        # Otherwise, delete after processing
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg["ReceiptHandle"]
        )
        print("Message deleted from queue.")
    
    print(messageList)
    return messageList


# Example usage:
if __name__ == "__main__":
    # Replace with your actual SQS queue URL
    queue_url = "https://sqs.us-east-1.amazonaws.com/216990846240/caleb-queue"
    receive_message_with_attributes(queue_url, max_messages=1, wait_time=5)
