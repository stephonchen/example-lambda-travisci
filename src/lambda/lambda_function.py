import boto3
import json
import time

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
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

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all running instances
    InstancesID = [instance.id for instance in instances]

    #make sure there are actually instances to shut down.
    if len(InstancesID) > 0:
        #perform EC2 actions
        if 'Power Up' == RequestBody['queryResult']['intent']['displayName']:
            EC2ActionStatus = ec2.instances.filter(InstanceIds=InstancesID).start()
        elif 'Power Down' == RequestBody['queryResult']['intent']['displayName']:
            EC2ActionStatus = ec2.instances.filter(InstanceIds=InstancesID).stop()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'time': CurrentTime,
                str(str(RequestBody['queryResult']['intent']['displayName']) + '_instances'): str(InstancesID)
            })
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'time': CurrentTime,
                str(str(RequestBody['queryResult']['intent']['displayName']) + '_instances'): "No any instances found, so no need to shutdown."
            })
        }
