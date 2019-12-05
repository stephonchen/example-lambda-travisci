import boto3
import json
import time

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Get current time
    CurrentTime = time.strftime("%Y-%m-%d %H:%M:%S")

    # Use request body instead of queryStrings
    RequestBody = event['body']

    # Use the filter() method of the instances collection to retrieve all instances
    filters = [
        {
            'Name': str('tag:' + RequestBody['tag']),
            'Values': [str(RequestBody['tag_value'])]
        },
        {
            'Name': 'instance-state-name',
            'Values': [str('running' if 'stop' == RequestBody['EC2Action'] or 'reboot' == RequestBody['EC2Action'] else 'stopped')]
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all running instances
    InstancesID = [instance.id for instance in instances]

    #make sure there are actually instances to shut down.
    if len(InstancesID) > 0:
        #perform EC2 actions
        if 'stop' == RequestBody['EC2Action']:
            EC2ActionStatus = ec2.instances.filter(InstanceIds=InstancesID).stop()
        elif 'start' == RequestBody['EC2Action']:
            EC2ActionStatus = ec2.instances.filter(InstanceIds=InstancesID).start()
        elif 'reboot' == RequestBody['EC2Action']:
            EC2ActionStatus = ec2.instances.filter(InstanceIds=InstancesID).reboot()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'time': CurrentTime,
                'debug': str(event),
                str(RequestBody['EC2Action'] + '_instances'): str(InstancesID)
            })
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'time': CurrentTime,
                'debug': str(event),
                str(RequestBody['EC2Action'] + '_instances'): "No any instances found, so no need to shutdown."
            })
        }
