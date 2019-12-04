import boto3
import json
import time

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Get current time
    CurrentTime = time.strftime("%Y-%m-%d %H:%M:%S")

    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
    filters = [{
            'Name': 'tag:Environment',
            'Values': ['Staging']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all running instances
    RunningInstances = [instance.id for instance in instances]

    #make sure there are actually instances to shut down.
    if len(RunningInstances) > 0:
        #perform the shutdown
        shuttingDown = ec2.instances.filter(InstanceIds=RunningInstances).stop()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'time': CurrentTime,
                'stopping_instances': str(RunningInstances)
            })
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'time': CurrentTime,
                'stopping_instances': "No any instances found, so no need to shutdown."
            })
        }
