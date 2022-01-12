import pandas as pd
import boto3
import json


from utils.helpers import api_response, bad_request

s3_client = boto3.client('s3')

def query_data(event, context):
    data = pd.read_csv('s3://owl-site-data/hero_data.csv')

    body = json.loads(event['body'])
    team_or_player = body.get('teamOrPlayer')
    x_num = body.get('xStatNum')
    x_denom = body.get('xStatDenom')
    y_num = body.get('yStatNum')
    y_denom = body.get('yStatDenom')

    if team_or_player is None or x_num is None or y_num is None:
        return bad_request('team_or_player, x_num, and y_num are required fields')

    teams = body.get('teams')
    players = body.get('players')
    stages = body.get('stages')
    oppo_teams = body.get('opponentTeams')
    comp = body.get('comp')
    oppo_comp = body.get('opponentComp')
    heroes = body.get('heroes')
    map_types = body.get('mapTypes')
    map_names = body.get('mapNames')


    if teams is not None:
        data = data[data['Team Name'].isin(teams)]

    if oppo_teams is not None:
        data = data[data['Opponent Team Name'].isin(oppo_teams)]

    if players is not None:
        data = data[data['Player'].isin(players)]

    if stages is not None:
        data = data[data['Stage'].isin(stages)]

    if map_types is not None:
        data = data[data['Map Type'].isin(map_types)]

    if map_names is not None:
        data = data[data['Map Name'].isin(map_names)]

    if comp is not None:
        data = data[data['Classification'] == comp]

    if oppo_comp is not None:
        data = data[data['Opponent Classification'] == oppo_comp]


    return api_response({
        'data': data
    })


"""
TODO: Add opponent comp, and opponent team to dataset

Add logic for filtering and aggregating data
DON'T FORGET PER 10
"""