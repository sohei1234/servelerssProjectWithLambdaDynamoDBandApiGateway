import datetime
import boto3
from boto3.session import Session
import json

def lambda_handler(event, context):
    region = "ap-northeast-1"
    session = Session(
        region_name=region
    )
    dynamodb = session.resource('dynamodb')

    table = dynamodb.Table('Person2')
    #print(event)
    put_response = table.put_item(
        Item = {
                #'timestamp': str(datetime.datetime.now().timestamp
                'username':event['username'],
                'telephone': event['telephone'],
                'country':event['country'],
                'city':event['city'],
                'street':event['street'],
                'register': str(datetime.datetime.utcnow())
                
    #print(event)
        }
    )
    scan_response = table.scan()
    #scan_response['Items'] = sorted(scan_response['Items'], key=lambda x:x['timestamp'], reverse=True)
    return scan_response