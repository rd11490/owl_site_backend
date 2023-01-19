import pandas as pd
import boto3
import json

from simulate.build_rmsa_map import build_rmsa_map, build_rmsa_map_coin_flip
from simulate.calculate_distribution import calculate_distribution
from simulate.calculate_tournament_table import calculate_tournament_table
from simulate.constants import Teams
from simulate.simulate_qualifiers import simulate_qualifiers

from utils.helpers import api_response
from utils.map_manual import map_manual, map_schedule

s3_client = boto3.client('s3')

"""
Body Format:
{
    simType: 'COIN' | 'RMSA' | 'CUSTOM'
    results: [
        {
            sim: True/False
            teamOne: str,
            teamOneWins?: int,
            teamTwo: str,
            teamTwoWins?: int,
        }
    ]


}
"""


def sim_stage(event, context):
    body = json.loads(event['body'])
    print(body)
    simType = body.get('simType')
    results = body.get('results')

    to_predict = [map_schedule(r) for r in results if r.get('sim') == True]
    manual = [r for r in results if r.get('sim') == False]
    manual_results = [map_manual(m) for m in manual]
    manual_results = pd.DataFrame(manual_results)

    if simType == 'RMSA':
        rmsa = pd.read_csv('s3://owl-site-data/ss_rmsa-2022.csv')
        rmsa = build_rmsa_map(rmsa)
    else:
        rmsa = build_rmsa_map_coin_flip()

    if len(to_predict) > 0:
        all_tables = simulate_qualifiers(pd.DataFrame(to_predict), manual_results, rmsa)
    else:
        all_tables = calculate_tournament_table(manual_results)
        all_tables['sim'] = 1
        all_tables['rank'] = list(range(1, len(Teams.West22) + 1))

    table = all_tables[['team', 'league_points', 'wins', 'losses', 'map_differential', 'rank']].groupby(
        'team').mean().reset_index()
    table = table.sort_values(by='rank').round(2)
    distribution = calculate_distribution(all_tables)

    return api_response({
        'table': table.to_dict('records'),
        'distribution': distribution.to_dict('records'),
    })



