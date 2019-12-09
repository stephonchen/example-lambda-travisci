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
    instances = ec2.instances.filter(Filters=filters)

    # locate all running instances
    InstancesID = [instance.id for instance in instances]

    # make sure there are actually instances to shut down.
    if len(InstancesID) > 0:
        # perform EC2 actions
        if 'Power Up' == RequestBody['queryResult']['intent']['displayName']:
            EC2ActionStatus = ec2.instances.filter(
                InstanceIds=InstancesID).start()
            response = sns.publish(
                TopicArn='arn:aws:sns:us-east-2:274867232613:polar-bear-chatbox-topic',
                Message='EC2 instance: '+str(InstancesID)+' was turned on.')
        elif 'Power Down' == RequestBody['queryResult']['intent']['displayName']:
            EC2ActionStatus = ec2.instances.filter(
                InstanceIds=InstancesID).stop()
            response = sns.publish(
                TopicArn='arn:aws:sns:us-east-2:274867232613:polar-bear-chatbox-topic', Message='EC2 instance: '+str(InstancesID)+' was turned off. You will save $0.0116 per hour.')
        return {
            'statusCode': 200,
            'body': json.dumps({
                'fulfillmentText': str(str(RequestBody['queryResult']['intent']['displayName']) + '_instances: ' + str(InstancesID))
            })
        }
    else:
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-2:274867232613:polar-bear-chatbox-topic', Message='No any instances found.')
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'fulfillmentText': 'No any instances found.'
            })
        }
