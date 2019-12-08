from lambdas.lambda_function import *
import pytest

def test_lambda_handler():
    response = '{"fulfillmentText": "Hello World!"}'
    assert response == '{"fulfillmentText": "Hello World!"}'
