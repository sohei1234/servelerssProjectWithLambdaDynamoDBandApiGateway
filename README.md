# servelerssProjectWithLambdaDynamoDBandApiGateway
DynamoDBにApigatewayをとしてLamdaFunctionからDataBaseのitem管理を行うプログラムの手順（python )

IAM Execution Role の作成

１．IAM console log in
２．左側にあるnavigation bar からPolicyをクリック
３．Create Policy
４．JSONタグを選択
５．以下を貼り付け
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "dynamodb:*",
                "logs:PutLogEvents",
                "dynamodb:DeleteBackup"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "*"
        },
        {
            "Sid": "Invoke",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": "arn:aws:lambda:ap-northeast-1:731647903955:function:SamplePostFunction"
        }
    ]
}
6. クリック review policy
7. name = LambdaBackupDynamoDBPolicy
８．Create

Role をつくり今作ったpolicy をattach

1.IAM naviagation bar から Role　を選択
２．create roles 
3. type of the trusted entity = AWS service
4. the service of use = Lambda
5. クッリク　next permmision 
6. LambdaBackupDynamoPolicyをサーチボックスから選択
7．next tag -> next Review
8. name = LambdaBackupDynamoDBRole
9. create 

続いてlumbda functions の製作

１．log in Lambda console 
2 . create function
3 . セレクト　Author from scratch 
4 . name = SamplePostFunction 
5 . runtime = Python3.7
6 . permission = choose ot create an execution role
7 . Execusion Role = LambdaBackupDynamoDBRole
8 . create function 
9 . paste the following code 

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

10 . save the script 
11 . test drop down の中から　configure test events を選択
12 . create a new test event 
13 . paste the following JSON code 
{
  "username": "soheiXYZ",
  "telephone": "09012402680",
  "country": "japan",
  "city": "laie",
  "street": "palekana"
}
14 . test 
15 . succeed code 200を確認
16．　dynamoDB 内に新しいitem がはいているか確認
以上が確認できればOK

APIGatewayの作成

1 . log in Apigateway console 
2 . create API
3 . choose protpcol = REST
4 . create new API = new API
5 . API name = 何でもOKです
6 . 今作ったAPIを選択
7 . Action drop button から create method を選択
8 . drop down から POST を選択
9 . integratioin type = lambda function 
10 . Lambda function = SamplePostFunction
11 . save 
12 . integration response を選択　method execution の中にあります。
13 . mapping template に行き　add mapping template を選択
14 . それぞれ Multipart/form-data, application/x-www-form-urlcoded　のファイルを作成（case sentitive)
15 . application/x-www-form-urlcodedに以下のコードを貼り付け
{
#set( $tmpstr = $input.body )
#foreach( $keyandvaluestr in $tmpstr.split( '&' ) )
#set( $keyandvaluearray = $keyandvaluestr.split( '=' ) )
        "$keyandvaluearray[0]" : "$keyandvaluearray[1]"
#end
}
16 . method execution に戻り　test をクリック
17 . copy and paste the following code request body の中に入れてください
{
  "username": "soheiXYZ",
  "telephone": "09012402680",
  "country": "japan",
  "city": "laie",
  "street": "palekana"
}
18 . status code が　２００であるのを確認
19 . Action drop button から　deploy を選択
20 . base = 何でもOK

他のmethod (delete, get, patch)はほぼ同じように作れます以下は違うところだけ手順を載せます
手順の12までは同じです
12 . integration request に行く
13 . mapping template 
14 . template name = application/json
15 . copy and paster the following code 
{
    "username": "$input.params("username")",
    "street":  "$input.params("street")",
    "city": "$input.params("city")",
    "telephone": "$input.params("telephone")",
    "country": "$input.params("country")"
}
16 . tset 
17 . body request ではなく query string に username = sohei&street= laieなどを入力

最終テスト
1 . RESTlet などのRESTAPI　test tool を用意
2 . Deploy で付与されたURLをコピペ
3 . sample body に以下をコピー
{
  "username": "soheiXYZ",
  "telephone": "09012402680",
  "country": "japan",
  "city": "laie",
  "street": "palekana"
}
4 . status 200 を確認





