import nltk
from nltk.corpus import wordnet
import boto3


def congifReader(file_name = "configFile.txt"):
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

    return URL, region, maxNumberOfMessage, waitTime, visibilityTimeout, maxConsecutiveErrors

def cipherSolver(encryptedText):
    nltk.download('wordnet')
    encryptedText = encryptedText.lower()

    for i in range(24):
        possibleWord = ""
        for j in encryptedText:
            if ord(j)+i > 122:
                possibleWord = possibleWord+chr(ord(j)+i-24)
            else:
                possibleWord = possibleWord+chr(ord(j)+i)
        
        print("is",possibleWord,"an english word? ",bool(wordnet.synsets(possibleWord)),"!")
        if bool(wordnet.synsets(possibleWord)):
            return possibleWord, i


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