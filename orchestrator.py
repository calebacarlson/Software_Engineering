import boto3
import time
import json

def send_sqs_message(message_body, queue_url, message_group_id=None, ):

    print("###",message_body,"###")

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
    print(params["MessageBody"])
    return response["MessageId"]

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
        game_num = next_line[1].strip("\n").strip(" ")
        print("game #",game_num)

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
                worker_order_dict[next_line[0]].append(next_line[1].strip())
            else:
                worker_order_dict[next_line[0]].append(next_line[1].strip())
            next_line = file.readline().split(',')


    return URL, region, game_num, waitTime, visibilityTimeout, maxConsecutiveErrors, worker_order_dict

            

def orchestrate_workers(worker_order_dict, game, waitTime):
    for key in worker_order_dict: # each level
        for job in worker_order_dict.get(key): # each worker in given level
            get_queue(job, game)
        wait_until_done(worker_order_dict.get(key), waitTime, game)

    result_jason = {
        "game-#": game,
        "worker-type": "game-as-a-whole",
        "status": "complete",
        "result": "DONE"
    }

    write_to_dynamodb(result_jason)
    
def write_to_dynamodb(item, table_name="caleb-carlson-result"):

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table(table_name)

    table.put_item(Item=item)

def get_queue(job, game):
    queue_look_up = {
        "cipher":"https://sqs.us-east-1.amazonaws.com/216990846240/caleb-carlson-cipher",
        "data":"https://sqs.us-east-1.amazonaws.com/216990846240/caleb-carlson-data",
        "logic":"https://sqs.us-east-1.amazonaws.com/216990846240/caleb-carlson-logic",
        "api_aggregator":"https://sqs.us-east-1.amazonaws.com/216990846240/caleb-carlson-api-aggregator"
    }

    queue_name = queue_look_up.get(job)

    job_index_look_up = {"cipher":0,"data":1, "logic":2, "api_aggregator":3}

    with open('workers.json', 'r') as file:
        data = json.load(file)
    
    message_body = ""

    for item in data["worker_types"][job_index_look_up.get(job)]:
        if data["worker_types"][job_index_look_up.get(job)][item] != job:
            message_body = message_body + data["worker_types"][job_index_look_up.get(job)][item] + "\n"

    message_body = message_body + game

    print(message_body, queue_name)
    send_sqs_message(message_body, queue_name)

def read_dynamodb_item(game, worker, table_name = "caleb-carlson-result"):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    print(game, worker, table_name)

    response = table.get_item(Key={"game-#":game, "worker-type":worker})["Item"]["status"]

    print("response!",response)

    return response

def wait_until_done(level_list, waitTime_str, game):
    waitTime = int(waitTime_str)
    worker_column_look_up = {"cipher":"cipher-worker", "data":"data-worker", "logic":"logic-worker", "api_aggregator":"api-aggregator-worker"}
    print(level_list)
    print(waitTime)
    print(game)
    for worker in level_list:
        print("WORKER",worker, worker_column_look_up.get(worker),"END")
        while True:
            try:
                respounce = read_dynamodb_item(game, worker_column_look_up.get(worker))
                if respounce == "complete":
                    break
            except:
                print("ZZZZZZZZzzzzzzzzz")
                print("waiting ",waitTime," seconds")
                time.sleep(waitTime)
                waitTime = waitTime * 2

                
            
            

send_sqs_message("{
  "table_name": "travis-puzzle-table",
  "item_key": "cipher_003",
  "task_type": "CIPHER"
}", "Travis-Cipher-Queue")

"""URL, region, game, waitTime, visibilityTimeout, maxConsecutiveErrors, worker_order_dict = congifReader()

orchestrate_workers(worker_order_dict, game, waitTime)"""





"""print(worker_order_dict)

# Reading JSON from a file
with open('workers.json', 'r') as file:
    data = json.load(file)

print(json.dumps(data, indent=4))
print(data["worker_types"][0]["table_name"])

"""