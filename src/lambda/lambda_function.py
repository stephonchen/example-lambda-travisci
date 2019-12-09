import boto3
import json
import time

# define the connection
ec2 = boto3.resource('ec2')
sns = boto3.client('sns')


def lambda_handler(event, context):
    # For test fulfillment
    if (not event or not context):
        return {
            'statusCode': 200,
            'body': json.dumps({
                'fulfillmentText': 'Hello World!'
            })
        }

    # Get current time
    CurrentTime = time.strftime("%Y-%m-%d %H:%M:%S")

    # Use request body instead of queryStrings
    RequestBody = json.loads(str(event['body']))

    # Use the filter() method of the instances collection to retrieve all instances
    filters = [
        {
            'Name': 'tag:Environment',
            'Values': ['Staging']
        },
        {
            'Name': 'instance-state-name',
            'Values': [str('stopped') if 'Power Up' == RequestBody['queryResult']['intent']['displayName'] else str('running')]
        }
    ]

    # filter the instances

    if 'list' == RequestBody['queryResult']['intent']['displayName']:
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}, {'Name': 'tag:Environment', 'Values': ['Staging']}])
        returnMessage = ''
        for instance in instances:
            returnMessage = returnMessage + '以下是已經被北極熊這隻熊控管的機器清單:' + \
                str(instance.id) + ' (' + str(instance.state) + ')\n'
        return {
            'statusCode': 200,
            'body': json.dumps({
                'fulfillmentText': returnMessage
            })
        }

    # locate all running instances
    instances = ec2.instances.filter(Filters=filters)
    InstancesID = [instance.id for instance in instances]

    # make sure there are actually instances to shut down.
    if len(InstancesID) > 0:
        # perform EC2 actions
        returnMessage = ''
        if 'Power Up' == RequestBody['queryResult']['intent']['displayName']:
            EC2ActionStatus = ec2.instances.filter(
                InstanceIds=InstancesID).start()
            returnMessage = '太棒了！你的 EC2 instance: ' + \
                str(InstancesID)+' 已經打開囉！！！幹活吧！少年機器開始運轉囉!就像我們的愛情摩天輪一樣！'
            response = sns.publish(
                TopicArn='arn:aws:sns:us-east-2:274867232613:polar-bear-chatbox-topic',
                Message=returnMessage)
        elif 'Power Down' == RequestBody['queryResult']['intent']['displayName']:
            EC2ActionStatus = ec2.instances.filter(
                InstanceIds=InstancesID).stop()
            returnMessage = '太棒了！你的 EC2 instance: ' + \
                str(InstancesID)+' 已經關掉了！！！洗洗睡吧！少年仔！你每天可以省下8美金喔！多多益善！發大財!'
            response = sns.publish(
                TopicArn='arn:aws:sns:us-east-2:274867232613:polar-bear-chatbox-topic', Message=returnMessage)
        return {
            'statusCode': 200,
            'body': json.dumps({'fulfillmentText': returnMessage})
        }
    else:
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-2:274867232613:polar-bear-chatbox-topic', Message='沒有符合機器拉！不要亂命令！')
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'fulfillmentText': '沒有符合機器拉！不要亂命令！'
            })
        }
