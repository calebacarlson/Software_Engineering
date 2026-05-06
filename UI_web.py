import webbrowser
from boto3.dynamodb.conditions import Attr
import boto3
import requests

path = input("which one do you want all-games (1), one-game(2), or default(any other key)")

def one_game(partition_key_value, partition_key_name="game-#", table_name="caleb-carlson-result"):

    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Perform query
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key(partition_key_name).eq(partition_key_value)
    )

    items = response.get('Items', [])

    # Handle pagination if there are more results
    while 'LastEvaluatedKey' in response:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key(partition_key_name).eq(partition_key_value),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response.get('Items', []))

    return items

def all_games(name="worker-type", sort_key_value="game-as-a-whole", table="caleb-carlson-result"):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)


    response = table.scan(
        FilterExpression=Attr(name).eq(sort_key_value)
    )
    items = response.get('Items', [])
    return items

def clean_format(json):
    clean_str = ""
    for i in range(len(json)):
        result = json[i]["result"]
        game_num = json[i]["game-#"]
        status = json[i]["status"]
        worker_type = json[i]["worker-type"]

        clean_str = clean_str+"Game number is "+game_num+"\nObject is "+worker_type+"\nStatus is "+status+"\nAnd finally result is "+result+"\n\n"
    return clean_str

def get_json_from_server(url, params=None):


    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
    
    # Parse JSON
    data = response.json()
    return data

if (path == "1"):
    url = "https://f9zppimwpe.us-east-1.awsapprunner.com/all_games"
    print(get_json_from_server(url))

elif (path == "2"):
    game_name = input("whats the name of the game? Ex. test-1, test-2")
    url = "https://f9zppimwpe.us-east-1.awsapprunner.com/one_game/"+game_name
    print(get_json_from_server(url))
else:
    url = "https://f9zppimwpe.us-east-1.awsapprunner.com"
    webbrowser.open(url)