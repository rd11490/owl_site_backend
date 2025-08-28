import pandas as pd

from utils.facit_tournaments import facit_tournaments, wara_tournaments
from utils.helpers import api_response


def get_faceit_rosters(event, context):
    import os
    bucket = os.environ.get('OWL_SITE_DATA_BUCKET')
    response_data = {}
    for key, value in facit_tournaments.items():
        rosters = pd.read_csv(f's3://{bucket}/{value[1]}.csv')
        rosters = rosters.fillna('')
        rosters_dict = rosters.to_dict('records')
        response_data[value[0]] = rosters_dict
    for key, value in wara_tournaments.items():
        rosters = pd.read_csv(f's3://{bucket}/{value[1]}.csv')
        rosters = rosters.fillna('')
        rosters_dict = rosters.to_dict('records')
        response_data[value[0]] = rosters_dict
    return api_response(response_data)
