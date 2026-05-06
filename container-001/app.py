import boto3
from flask import Flask, jsonify
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>the orchestrator sends messages to the workers queue (caleb-carlson-cipher, caleb-carlson-data, caleb-carlson-logic and caleb-carlson-api-aggregator).The queue messages needs to be formatted as such (caleb-carlson-cipher & caleb-carlson-logic: table-name on first line game-# on second) the table I use is named caleb-carlson table. (caleb-carlson-data: bucket-name on first line file-name on second and game-# on the third line) The bucket I use is named caleb-carlson-bucket and it has a data.txt file with numbers on each line. (caleb-carlson-api-aggregator: first line has game-#) Once the workers are done they will send the results to a table named caleb-carlson-result. This web server pulls information from that table</h1>"

@app.route("/all_games")
def all_games_route():
    return jsonify(clean_format(all_games()))

@app.route("/one_game/<game>")
def one_game_route(game):
    return jsonify(clean_format(one_game(game)))

def all_games(name="worker-type", sort_key_value="game-as-a-whole", table="caleb-carlson-result"):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)


    response = table.scan(
        FilterExpression=Attr(name).eq(sort_key_value)
    )
    items = response.get('Items', [])
    print(f"Found {len(items)} items:", items)
    return items

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
    print(f"Found {len(items)} items:", items)

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

if __name__ == "__main__":
    # Bind to 0.0.0.0 so it works inside Docker
    app.run(host="0.0.0.0", port=3000)
