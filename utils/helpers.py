import json
from re import split

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': True
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

def camelize(string):
        s = ''.join([a.capitalize() for a in split('([^a-zA-Z0-9])', string) if a.isalnum()])
        return s[0].lower() + s[1:]