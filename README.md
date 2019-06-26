# servelerssProjectWithLambdaDynamoDBandApiGateway
DynamoDBにApigatewayをとしてLamdaFunctionからDataBaseのitem管理を行うプログラムの手順（python )

IAM Execution Role の作成

１．IAM console log in<br>
２．左側にあるnavigation bar からPolicyをクリック<br>
３．Create Policy<br>
４．JSONタグを選択<br>
５．以下を貼り付け<br>
{<br>
    "Version": "2012-10-17",<br>
    "Statement": [<br>
        {<br>
            "Sid": "VisualEditor0",<br>
            "Effect": "Allow",<br>
            "Action": [<br>
                "logs:CreateLogStream",<br>
                "dynamodb:*",<br>
                "logs:PutLogEvents",<br>
                "dynamodb:DeleteBackup"<br>
            ],<br>
            "Resource": "*"<br>
        },<br>
        {<br>
            "Sid": "VisualEditor1",<br>
            "Effect": "Allow",<br>
            "Action": "logs:CreateLogGroup",<br>
            "Resource": "*"<br>
        },<br>
        {<br>
            "Sid": "Invoke",<br>
            "Effect": "Allow",<br>
            "Action": [<br>
                "lambda:InvokeFunction"<br>
            ],<br>
            "Resource": "arn:aws:lambda:ap-northeast-1:731647903955:function:SamplePostFunction"<br>
        }<br>
    ]<br>
}<br>
6. クリック review policy<br>
7. name = LambdaBackupDynamoDBPolicy<br>
８．Create<br>

Role をつくり今作ったpolicy をattach<br>

1.IAM naviagation bar から Role　を選択<br>
２．create roles <br>
3. type of the trusted entity = AWS service<br>
4. the service of use = Lambda<br>
5. クッリク　next permmision <br>
6. LambdaBackupDynamoPolicyをサーチボックスから選択<br>
7．next tag -> next Review<br>
8. name = LambdaBackupDynamoDBRole<br>
9. create <br>

続いてlumbda functions の製作<br>

１．log in Lambda console <br>
2 . create function<br>
3 . セレクト　Author from scratch<br> 
4 . name = SamplePostFunction <br>
5 . runtime = Python3.7<br>
6 . permission = choose ot create an execution role<br>
7 . Execusion Role = LambdaBackupDynamoDBRole<br>
8 . create function <br>
9 . paste the following code<br> 

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

10 . save the script <br>
11 . test drop down の中から　configure test events を選択<br>
12 . create a new test event <br>
13 . paste the following JSON code<br> 
{<br>
  "username": "soheiXYZ",<br>
  "telephone": "09012402680",<br>
  "country": "japan",<br>
  "city": "laie",<br>
  "street": "palekana"<br>
}<br>
14 . test <br>
15 . succeed code 200を確認<br>
16．　dynamoDB 内に新しいitem がはいているか確認<br>
以上が確認できればOK<br>

APIGatewayの作成<br>

1 . log in Apigateway console<br> 
2 . create API<br>
3 . choose protpcol = REST<br>
4 . create new API = new API<br>
5 . API name = 何でもOKです<br>
6 . 今作ったAPIを選択<br>
7 . Action drop button から create method を選択<br>
8 . drop down から POST を選択<br>
9 . integratioin type = lambda function<br> 
10 . Lambda function = SamplePostFunction<br>
11 . save <br>
12 . integration response を選択　method execution の中にあります。<br>
13 . mapping template に行き　add mapping template を選択<br>
14 . それぞれ Multipart/form-data, application/x-www-form-urlcoded　のファイルを作成（case sentitive)<br>
15 . application/x-www-form-urlcodedに以下のコードを貼り付け<br>
{
#set( $tmpstr = $input.body )
#foreach( $keyandvaluestr in $tmpstr.split( '&' ) )
#set( $keyandvaluearray = $keyandvaluestr.split( '=' ) )
        "$keyandvaluearray[0]" : "$keyandvaluearray[1]"
#end
}
16 . method execution に戻り　test をクリック<br>
17 . copy and paste the following code request body の中に入れてください<br>
{<br>
  "username": "soheiXYZ",<br>
  "telephone": "09012402680",<br>
  "country": "japan",<br>
  "city": "laie",<br>
  "street": "palekana"<br>
}<br>
18 . status code が　２００であるのを確認<br>
19 . Action drop button から　deploy を選択<br>
20 . base = 何でもOK<br>

他のmethod (delete, get, patch)はほぼ同じように作れます以下は違うところだけ手順を載せます<br>
手順の12までは同じです<br>
12 . integration request に行く<br>
13 . mapping template <br>
14 . template name = application/json<br>
15 . copy and paster the following code <br>
{<br>
  "username": "soheiXYZ",<br>
  "telephone": "09012402680",<br>
  "country": "japan",<br>
  "city": "laie",<br>
  "street": "palekana"<br>
}<br>
16 . tset <br>
17 . body request ではなく query string に username = sohei&street= laieなどを入力<br>

最終テスト<br>
1 . RESTlet などのRESTAPI　test tool を用意<br>
2 . Deploy で付与されたURLをコピペ<br>
3 . sample body に以下をコピー<br>
{<br>
  "username": "soheiXYZ",<br>
  "telephone": "09012402680",<br>
  "country": "japan",<br>
  "city": "laie",<br>
  "street": "palekana"<br>
}<br>
4 . status 200 を確認<br>





