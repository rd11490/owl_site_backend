import pandas as pd
import boto3
import json


from utils.helpers import api_response, bad_request

s3_client = boto3.client('s3')

def query_data(event, context):
    data = pd.read_csv('s3://owl-site-data/hero_data.csv')

    body = json.loads(event['body'])
    print(body)
    aggregation = body.get('aggregation')

    if aggregation is None or aggregation not in ['TEAM', 'PLAYER', 'HERO']:
        return bad_request('aggregation must be set')

    teams = body.get('teams')
    players = body.get('players')
    stages = body.get('stages')
    oppo_teams = body.get('opponentTeams')
    comp = body.get('composition')
    oppo_comp = body.get('opponentComposition')
    map_types = body.get('mapTypes')
    map_names = body.get('mapNames')
    heroes = body.get('heroes')
    stats = body.get('stats')

    if teams:
        data = data[data['Team Name'].isin(teams)]

    if oppo_teams:
        data = data[data['Opponent Team Name'].isin(oppo_teams)]

    if players:
        data = data[data['Player'].isin(players)]

    if stages:
        data = data[data['Stage'].isin(stages)]

    if map_types:
        data = data[data['Map Type'].isin(map_types)]

    if map_names:
        data = data[data['Map Name'].isin(map_names)]

    if comp is not None:
        data = data[data['Classification'] == comp]

    if oppo_comp is not None:
        data = data[data['Opponent Classification'] == oppo_comp]

    if heroes:
        data = data[data['Hero'].isin(heroes)]

    if stats:
        data = data[data['Stat'].isin(stats)]

    if aggregation == 'PLAYER':
        data = data[['Player', 'Stat', 'Amount']].groupby(
            by=['Player', 'Stat']).sum().reset_index()
        data = data.pivot(index='Player', columns='Stat', values='Amount').fillna(0.0).reset_index()
    elif aggregation == 'TEAM':
        data = data[['Team Name', 'Stat', 'Amount']].groupby(
            by=['Team Name', 'Stat']).sum().reset_index()
        data = data.pivot(index='Team Name', columns='Stat', values='Amount').fillna(0.0).reset_index()
    elif aggregation == 'HERO':
        data = data[['Hero', 'Stat', 'Amount']].groupby(
            by=['Hero', 'Stat']).sum().reset_index()
        data = data.pivot(index='Hero', columns='Stat', values='Amount').fillna(0.0).reset_index()


    data = data.round(2)
    return api_response({
        'data': data.to_dict('records')
    })

