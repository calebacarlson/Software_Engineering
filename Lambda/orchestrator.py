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

        messageList.append([idx, msg.get('MessageId'), msg.get('Body'), msg.get('Attributes'), msg.get('MessageAttributes')])

        # If you don't want to delete the message, skip this step
        # Otherwise, delete after processing
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg["ReceiptHandle"]
        )
        print("Message deleted from queue.")
    
    print(messageList)
    return messageList

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

def congifReader(file_name = "Lambda\\configFile.txt"):
    URL = ""
    region = ""
    maxNumberOfMessage = ""
    waitTime = ""
    visibilityTimeout = ""
    maxConsecutiveErrors = ""

    with open(file_name,'r') as file:

        next_line = file.readline().split(',')
        URL = next_line[1].strip("\n").strip(" ")
        print("URL",URL)

        next_line = file.readline().split(',')
        region = next_line[1].strip("\n").strip(" ")
        print("region",region)

        next_line = file.readline().split(',')
        maxNumberOfMessage = next_line[1].strip("\n").strip(" ")
        print("maxNumberOfMessage",maxNumberOfMessage)

        next_line = file.readline().split(',')
        waitTime = next_line[1].strip("\n").strip(" ")
        print("waitTime",waitTime)

        next_line = file.readline().split(',')
        visibilityTimeout = next_line[1].strip("\n").strip(" ")
        print("visibilityTimeout",visibilityTimeout)

        next_line = file.readline().split(',')
        maxConsecutiveErrors = next_line[1].strip("\n").strip(" ")
        print("maxConsecutiveErrors",maxConsecutiveErrors)



        worker_order_dict = {}
        next_line = file.readline()
        next_line = file.readline().split(',')
        while next_line != ['']:
            if next_line[0] not in worker_order_dict:
                worker_order_dict[next_line[0]] = []
                worker_order_dict[next_line[0]].append(next_line[1])
            else:
                worker_order_dict[next_line[0]].append(next_line[1])
            next_line = file.readline().split(',')


    return URL, region, maxNumberOfMessage, waitTime, visibilityTimeout, maxConsecutiveErrors, worker_order_dict

URL, region, maxNumberOfMessage, waitTime, visibilityTimeout, maxConsecutiveErrors, worker_order_dict = congifReader()

print(worker_order_dict)