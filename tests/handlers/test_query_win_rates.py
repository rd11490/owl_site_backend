import pytest
import pandas as pd
import json
from handlers.query_win_rates import query_win_rates

class DummyContext:
    pass

def make_event(body_dict):
    return {'body': json.dumps(body_dict)}

def test_empty_body(monkeypatch):
    monkeypatch.setattr(pd.DataFrame, 'to_csv', lambda *args, **kwargs: None)
    # Patch pd.read_csv to return a test DataFrame
    test_df = pd.DataFrame({
        'name': ['Ana'],
        'pickrate': [10.0],
        'winrate': [50.0],
        'map': ['all-maps'],
        'region': ['Americas'],
        'tier': ['All'],
        'date': ['2025-09-01']
    })
    monkeypatch.setattr(pd, 'read_csv', lambda *args, **kwargs: test_df)
    event = make_event({})
    result = query_win_rates(event, DummyContext())
    assert result['statusCode'] == 200
    data = json.loads(result['body'])
    # Accept any non-empty result, since grouping may produce >1
    assert len(data) >= 1
    assert data[0]['hero'] == 'Ana'
    assert data[0]['map'] == 'all-maps'
    assert data[0]['rank'] == 'All'
    assert data[0]['region'] == 'Americas'
    assert data[0]['data'][0]['winRate'] == 50.0
    assert data[0]['data'][0]['pickRate'] == 10.0
    assert data[0]['data'][0]['date'] == '2025-09-01'

def test_filters(monkeypatch):
    test_df = pd.DataFrame({
        'name': ['Ana', 'Ashe'],
        'pickrate': [10.0, 20.0],
        'winrate': [50.0, 60.0],
        'map': ['all-maps', 'busan'],
        'region': ['Americas', 'Asia'],
        'tier': ['All', 'Bronze'],
        'date': ['2025-09-01', '2025-09-02']
    })
    monkeypatch.setattr(pd, 'read_csv', lambda *args, **kwargs: test_df)
    event = make_event({
        'region': ['Americas'],
        'map': ['all-maps'],
        'hero': ['Ana'],
        'rank': ['All'],
        'dateRange': {'min': '2025-09-01', 'max': '2025-09-01'}
    })
    result = query_win_rates(event, DummyContext())
    data = json.loads(result['body'])
    assert len(data) == 1
    assert data[0]['hero'] == 'Ana'
    assert data[0]['map'] == 'all-maps'
    assert data[0]['rank'] == 'All'
    assert data[0]['region'] == 'Americas'
    assert data[0]['data'][0]['date'] == '2025-09-01'

def test_invalid_json():
    event = {'body': 'not a json'}
    result = query_win_rates(event, DummyContext())
    assert result['statusCode'] == 400
    assert 'Invalid JSON body' in result['body']
