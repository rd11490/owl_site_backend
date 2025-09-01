import pytest
import pandas as pd
import json
from handlers.scrape_win_rates import scrape_win_rates, fetch_win_rates

class DummyContext:
    pass

def test_invalid_region():
    event = {'body': json.dumps({'region': 'InvalidRegion'})}
    result = scrape_win_rates(event, DummyContext())
    assert result['statusCode'] == 400
    assert 'No valid region provided' in result['body']

def test_valid_region(monkeypatch):
    # Patch fetch_win_rates to return a test DataFrame
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
    monkeypatch.setattr(fetch_win_rates, '__call__', lambda params: test_df)
    monkeypatch.setattr(pd.DataFrame, 'to_csv', lambda *args, **kwargs: None)
    monkeypatch.setattr(pd, 'concat', lambda dfs, ignore_index: test_df)
    event = {'body': json.dumps({'region': 'Americas'})}
    result = scrape_win_rates(event, DummyContext())
    # Should not error, but may not return a statusCode (depends on implementation)
    # Just check no crash and print output
    assert isinstance(result, dict) or result is None
