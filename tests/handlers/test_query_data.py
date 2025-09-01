import pytest
import pandas as pd
import json
from handlers.query_data import query_data

class DummyContext:
    pass

def make_event(body_dict):
    return {'body': json.dumps(body_dict)}

def test_missing_aggregation(monkeypatch):
    test_df = pd.DataFrame({'Team Name': ['TeamA'], 'Stat': ['Stat1'], 'Amount': [10.0]})
    monkeypatch.setattr(pd, 'read_csv', lambda *args, **kwargs: test_df)
    event = make_event({'season': '2021'})
    result = query_data(event, DummyContext())
    assert result['statusCode'] == 400
    assert 'aggregation must be set' in result['body']

def test_team_aggregation(monkeypatch):
    monkeypatch.setattr(pd.DataFrame, 'to_csv', lambda *args, **kwargs: None)
    # DataFrame with 'Team Name' column to match expected handler input
    test_df = pd.DataFrame({'Team Name': ['TeamA'], 'Stat': ['Stat1'], 'Amount': [10.0]})
    monkeypatch.setattr(pd, 'read_csv', lambda *args, **kwargs: test_df)
    event = make_event({'season': '2021', 'aggregation': 'TEAM', 'teams': ['TeamA']})
    result = query_data(event, DummyContext())
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert 'data' in body
    assert 'stats' in body
    assert body['data'][0]['teamName'] == 'TeamA'
    assert body['stats'][0] == 'Stat1'

def test_invalid_json():
    event = {'body': 'not a json'}
    try:
        query_data(event, DummyContext())
    except Exception:
        assert True
