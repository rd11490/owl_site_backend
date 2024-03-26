import pandas as pd
import boto3

from utils.helpers import api_response

s3_client = boto3.client('s3')

def get_circuit_points(event, context):

    emea_points = pd.read_csv('s3://owl-site-data/emea_circuit_points.csv')
    emea_dict = emea_points.to_dict('records')

    na_points = pd.read_csv('s3://owl-site-data/na_circuit_points.csv')
    na_dict = na_points.to_dict('records')

    return api_response({
        'na_points': na_dict,
        'emea_points': emea_dict
    })
