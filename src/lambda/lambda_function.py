import boto3
import json
import time

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Get current time
    CurrentTime = time.strftime("%Y-%m-%d %H:%M:%S")

    # 'queryStringParameters': {'tag_value': 'Staging', 'tag': 'Environment', 'EC2Action': 'start/stop/reboot'}
    parameters = event['queryStringParameters']

    # Use the filter() method of the instances collection to retrieve all instances
    filters = [
        {
            'Name': str('tag:' + parameters['tag']),
            'Values': [str(parameters['tag_value'])]
        },
        {
            'Name': 'instance-state-name',
            'Values': [str('stopped' if 'stop' == parameters['EC2Action'] else 'running')]
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all running instances
    InstancesID = [instance.id for instance in instances]

    #make sure there are actually instances to shut down.
    if len(InstancesID) > 0:
        #perform EC2 actions
        if 'stop' == parameters['EC2Action']:
            EC2ActionStatus = ec2.instances.filter(InstanceIds=InstancesID).stop()
        elif 'start' == parameters['EC2Action']:
            EC2ActionStatus = ec2.instances.filter(InstanceIds=InstancesID).start()
        elif 'reboot' == parameters['EC2Action']:
            EC2ActionStatus = ec2.instances.filter(InstanceIds=InstancesID).reboot()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'time': CurrentTime,
                'debug': str(filters),
                str(parameters['EC2Action'] + '_instances'): str(InstancesID)
            })
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'time': CurrentTime,
                'debug': str(filters),
                str(parameters['EC2Action'] + '_instances'): "No any instances found, so no need to shutdown."
            })
        }
