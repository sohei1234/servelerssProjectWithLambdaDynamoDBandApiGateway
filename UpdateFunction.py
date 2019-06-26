import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    tName='Person2'
    table = dynamodb.Table(tName)
    if event['city']!='':    
        table.update_item(
            Key={
                'username': event['username']
            },
            UpdateExpression='SET city = :val1',
            ExpressionAttributeValues={
                ':val1': event['city']
            }
        )
        
    elif event['street']!='':
        table.update_item(
            Key={
                'username': event['username']
            },
            UpdateExpression='SET street = :val1',
            ExpressionAttributeValues={
                ':val1': event['street']
            }
        )
    elif event['country']!='':
        table.update_item(
            Key={
                'username': event['username']
            },
            UpdateExpression='SET country = :val1',
            ExpressionAttributeValues={
                ':val1': event['country']
            }
        )
    elif event['telephone']!='':
        table.update_item(
            Key={
                'username': event['username']
            },
            UpdateExpression='SET telephone = :val1',
            ExpressionAttributeValues={
                ':val1': event['telephone']
            }
        )
    elif event['email']!='':
        table.update_item(
            Key={
                'username': event['username']
            },
            UpdateExpression='SET email = :val1',
            ExpressionAttributeValues={
                ':val1': event['email']
            }
        )
    table.update_item(
            Key={
                'username': event['username']
            },
            UpdateExpression='SET updateDate=:val1',
            ExpressionAttributeValues={
                ':val1': str(datetime.datetime.utcnow())
            }
        )
       
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
