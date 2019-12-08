import sys
import boto3
sys.path.insert(0, '../src/lambda')
from lambda_function import *

def test_lambda_handler(event_context):
    event = []
    context = []
    response = lambda_handler(event, context)
    assert response == '{"fulfillmentText": "Hello World!"}'
