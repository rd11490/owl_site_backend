import pandas as pd
import os
import json
from utils.constants import REGION_LIST, TIER_LIST, MAP_LIST, HERO_LIST
from utils.helpers import api_response, bad_request

def query_win_rates(event, context):
    # Parse and validate input
    try:
        body = json.loads(event.get('body', '{}'))
    except Exception:
        return bad_request('Invalid JSON body')

    date_range = body.get('dateRange', {})
    min_date = date_range.get('min')
    max_date = date_range.get('max')
    regions = body.get('region', REGION_LIST)
    maps = body.get('map', ['all-maps'])
    heroes = body.get('hero', HERO_LIST)
    ranks = body.get('rank', ['All'])

    # If rank or map is null or empty, use ['All']
    if not ranks:
        ranks = ['All']
    if not maps:
        maps = ['all-maps']

    bucket = os.environ.get('OWL_SITE_DATA_BUCKET', 'owl-site-data')
    results = []

    for region in regions:
        s3_path = f's3://{bucket}/overwatch_win_rates_{region.lower()}.csv'
        try:
            df = pd.read_csv(s3_path)
        except Exception as e:
            print(f"Error reading {s3_path}: {e}")
            continue

        # Apply filters
        if min_date:
            df = df[df['date'] >= min_date]
        if max_date:
            df = df[df['date'] <= max_date]
        if maps:
            df = df[df['map'].isin(maps)]
        if heroes:
            df = df[df['name'].isin(heroes)]
        if ranks:
            df = df[df['tier'].isin(ranks)]

        # Group and format results
        grouped = df.groupby(['name', 'tier', 'map', 'region'])
        for (hero, rank, map_name, region_name), group in grouped:
            group_sorted = group.sort_values('date')
            data = [
                {
                    'winRate': row['winrate'],
                    'pickRate': row['pickrate'],
                    'date': row['date']
                }
                for _, row in group_sorted.iterrows()
            ]
            results.append({
                'hero': hero,
                'map': map_name,
                'rank': rank,
                'region': region_name,
                'data': data
            })

    return api_response(results)
