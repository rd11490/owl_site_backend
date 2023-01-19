import pandas as pd
import boto3

from simulate.calculate_distribution import calculate_distribution
from simulate.calculate_tournament_table import calculate_tournament_table
from simulate.constants import Teams
from utils.helpers import api_response

s3_client = boto3.client('s3')


def get_schedule(event, context):
    schedule = pd.read_csv('s3://owl-site-data/2022_league_schedule.csv')
    results = pd.read_csv('s3://owl-site-data/2022_ss_manual_results.csv')
    schedule_resp = schedule.to_dict('records')
    results_rsp = results.to_dict('records')

    all_tables = calculate_tournament_table(results)
    all_tables['sim'] = 1
    all_tables['rank'] = list(range(1, len(Teams.West22) + 1))


    table = all_tables[['team', 'league_points', 'wins', 'losses', 'map_differential', 'rank']].groupby('team').mean().reset_index()
    table = table.sort_values(by='rank').round(2)
    distribution = calculate_distribution(all_tables)

    return api_response({
        'results': results_rsp,
        'schedule': schedule_resp,
        'table': table.to_dict('records'),
        'distribution': distribution.to_dict('records')
    })
