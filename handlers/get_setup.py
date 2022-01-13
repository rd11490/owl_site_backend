import pandas as pd
import boto3

from utils.helpers import api_response

s3_client = boto3.client('s3')

def get_setup(event, context):
    players = pd.read_csv('s3://owl-site-data/teams_players.csv')
    player_resp = players.to_dict('records')

    comps = pd.read_csv('s3://owl-site-data/comps_list.csv')
    comp_resp = comps.to_dict('records')

    teams = players['teamName'].unique().tolist()
    stats = pd.read_csv('s3://owl-site-data/stats.csv')['Stat'].unique().tolist()
    stages = pd.read_csv('s3://owl-site-data/stage.csv')['Stage'].unique().tolist()
    map_types = pd.read_csv('s3://owl-site-data/map_types.csv')['Map Type'].unique().tolist()
    map_names = pd.read_csv('s3://owl-site-data/map_names.csv')['Map Name'].unique().tolist()
    heroes = pd.read_csv('s3://owl-site-data/heroes.csv')['Hero'].unique().tolist()

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
