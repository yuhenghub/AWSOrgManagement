import boto3
import json
import os

logs_bucket = os.environ['logs_bucket']
record = 'record.json'
_TopicArn_ = os.environ['SNS_ARN']

def list_records_format():
    client = boto3.client('organizations')
    accounts = client.list_accounts()
    # print(accounts['Accounts'],type(accounts['Accounts']))
    article_info = []
    for entity in accounts['Accounts']:
        # print(entity['Id'])
        article_info.append(entity['Id'])
    record = json.dumps(article_info,default=str)
    return json.loads(record)

def list_records():
    client = boto3.client('organizations')
    accounts = client.list_accounts()
    # print(accounts['Accounts'],type(accounts['Accounts']))
    article_info = []
    for entity in accounts['Accounts']:
        # print(entity['Id'])
        article_info.append(entity['Id'])
    record = json.dumps(article_info,default=str)
    return record

def read_records():
    client = boto3.client('s3')
    try:
        result = client.get_object(Bucket=logs_bucket, Key=record)
        content = result['Body']
        jsonObject = json.loads(content.read())

        return jsonObject
    except Exception as e:
        if str(e) == 'An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist.':
            write_records(list_records())

            result = client.get_object(Bucket=logs_bucket, Key=record)
            content = result['Body']
            jsonObject = json.loads(content.read())

            return jsonObject

def write_records(new_record:json):
    client = boto3.client('s3')
    client.put_object(Body=new_record, Bucket=logs_bucket, Key=record)

def sns_push_message(memberaccount):
    client = boto3.client('sns')
    response = client.publish(
        TopicArn = _TopicArn_,
        Message='有账号离开了组织，账号为：{}'.format(memberaccount),
        Subject='Leave Org Alert from Customer A on Member Account {}'.format(memberaccount)
    )

def lambda_handler(event, context):
    # print(list_records())
    # write_records(list_records())
    # print(read_records())

    a = list_records_format()
    b = read_records()

    # print(set(a).difference(set(b))) #差集，在list1中但不在list2中的元素)

    addValue = set(a).difference(set(b)) #差集，在a中但不在b中的元素)
    deleteValue = set(b).difference(set(a)) #差集，在b中但不在a中的元素
    # print(addValue,type(addValue)) #差集，在list2中但不在list1中的元素
    if len(deleteValue) == 0 :
        print('1111111') # 表示新数据中没有少
    else:
        # print(deleteValue)
        for i in list(deleteValue):
            print(i)
            # 发送邮件
            sns_push_message(i)


    # 将新纪录写入s3
    write_records(list_records())