import boto3

def delete_dynamodb_table(table_name, region="us-east-1"):
    dynamodb = boto3.client("dynamodb", region_name=region)
    dynamodb.delete_table(TableName=table_name)

def read_taskman_config(file_name):
    task = ""
    object_name = ""

    with open(file_name,'r') as file:
        next_line = file.readline().split(',')
        task = next_line[1].strip("\n").strip(" ")
        next_line = file.readline().split(',')
        object_name = next_line[1]
        print("task",">"+task+"<")
        print("object_name",object_name)
    return task, object_name

task, object_name = read_taskman_config("taskman.txt")

if task == "delete":
    print("DELETING")
    delete_dynamodb_table("delete-me-again")
else:
    print("NO TASK FOUND")