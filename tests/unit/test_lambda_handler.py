from lambda.lambda_function import *
import pytest

def test_lambda_handler(event_context):
    event = []
    context = []
    response = lambda_handler(event, context)
    assert response == '{"fulfillmentText": "Hello World!"}'
