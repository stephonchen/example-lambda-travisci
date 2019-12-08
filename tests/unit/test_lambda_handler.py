import sys
import boto3
sys.path.insert(0, '../src/lambda')
import lambda_function

def test_lambda_handler(event_context):
    event = []
    context = []
    response = lambda_handler(event, context)
    assert response == '{"fulfillmentText": "Hello World!"}'
