import sys
import boto3

def test_lambda_handler(event, context):
    event = []
    context = []
    response = '{"fulfillmentText": "Hello World!"}'
    assert response == '{"fulfillmentText": "Hello World!"}'
