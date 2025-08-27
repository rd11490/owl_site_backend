import pandas as pd
import boto3
import os

from utils.helpers import api_response

s3_client = boto3.client('s3')


def get_setup(event, context):
    qp = event.get('queryStringParameters')
    if qp is None:
        season_tag = ''
    else:
        season = qp.get('season')
        if season in ['2018', '2019', '2020', '2022', '2023']:
            season_tag = f'_{season}'
        else:
            season_tag = ''
    
    bucket = os.environ.get('OWL_SITE_DATA_BUCKET', 'owl-site-data')
    players = pd.read_csv(f's3://{bucket}/teams_players{season_tag}.csv')
    player_resp = players.to_dict('records')

    comps = pd.read_csv(f's3://{bucket}/comps_list{season_tag}.csv')
    comp_resp = comps.to_dict('records')

    teams = players['teamName'].unique().tolist()
    stats = pd.read_csv(f's3://{bucket}/stats{season_tag}.csv')['Stat'].unique().tolist()
    stages = pd.read_csv(f's3://{bucket}/stage{season_tag}.csv')['Stage'].unique().tolist()
    map_types = pd.read_csv(f's3://{bucket}/map_types{season_tag}.csv')['Map Type'].unique().tolist()
    map_names = pd.read_csv(f's3://{bucket}/map_names{season_tag}.csv')['Map Name'].unique().tolist()
    heroes = pd.read_csv(f's3://{bucket}/heroes{season_tag}.csv')['Hero'].unique().tolist()
    
    return api_response({
    'comps': comp_resp,
    'heroes': heroes,
    'mapNames': map_names,
    'mapTypes': map_types,
    'players': player_resp,
    'stats': stats,
    'stages': stages,
    'teams': teams
    })
