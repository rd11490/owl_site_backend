import json
from datetime import datetime

headers = {
    'Access-Control-Allow-Origin': '*'
}

def api_response(body):
    return {
        'statusCode': 200,
        'body': json.dumps(body),
        'headers': headers
    }

def bad_request(body):
    return {
        'statusCode': 400,
        'body': body,
        'headers': headers
    }