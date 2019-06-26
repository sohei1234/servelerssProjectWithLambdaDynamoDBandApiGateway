import datetime
import boto3
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr
import time
import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, contect):
    region = "ap-northeast-1"
    session = Session(
        region_name=region
        )
    dynamodb= session.resource('dynamodb')
    
    table = dynamodb.Table('Person2')
    print(event)
    
    #if event['test_id'] != '':
    
    if event['username'] !='' and event['city'] !='':
        response = table.query(
            IndexName='staffindex',
            KeyConditionExpression=Key('username').eq(event['username']) & Key('city').eq(event['city'])
            
        )
    elif event['username'] !='' and event['street'] !='':
        response = table.query(
            IndexName='streetIndex',
            KeyConditionExpression=Key('username').eq(event['username']) & Key('street').eq(event['street'])
            
        )
    elif event['username'] !='' and event['country']!='':
        response = table.query(
            IndexName='countryIndex',
            KeyConditionExpression=Key('username').eq(event['username']) & Key('country').eq(event['country'])
            
        )
    elif event['username'] !='' and event['telephone']!='':
        response = table.query(
            IndexName='telephoneIndex',
            KeyConditionExpression=Key('username').eq(event['username']) & Key('telephone').eq(event['telephone'])
            
        )
    elif event['username']!='':
        response = table.query(
            KeyConditionExpression=Key('username').eq(event['username'])
            
        )

    items = response['Items']
    
    return response
    