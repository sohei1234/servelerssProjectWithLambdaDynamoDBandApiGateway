import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Person2')
        
    if event['username'] !='' and event['city'] !='':
        table.delete_item(
            Key={
                'username':event['username']
            },
            ConditionExpression="city <= :val",
            ExpressionAttributeValues={
                ":val":event['city']
            }
        )
    elif event['username'] !='' and event['street'] !='':
        table.delete_item(
            Key={
                'username':event['username']
            },
            ConditionExpression="street <= :val",
            ExpressionAttributeValues={
                ":val":event['street']
            }
        )
    elif event['username'] !='' and event['country'] !='':
        table.delete_item(
            Key={
                'username':event['username']
            },
            ConditionExpression="country <= :val",
            ExpressionAttributeValues={
                ":val":event['country']
            }
        )
    elif event['username'] !='' and event['telephone'] !='':
        table.delete_item(
            Key={
                'username':event['username']
            },
            ConditionExpression="telephone <= :val",
            ExpressionAttributeValues={
                ":val":event['telephone']
            }
        )
    elif event['username'] !='':
        table.delete_item(
            Key={
                'username':event['username']
            }
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
