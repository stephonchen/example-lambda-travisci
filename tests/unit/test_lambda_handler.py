import pytest

def test_lambda_handler(event_context):
    return {
        "fulfillmentText": "Hello World!"
    }

if __name__ == "__main__":
    event = []
    context = []
    test_lambda_handler(event, context)
