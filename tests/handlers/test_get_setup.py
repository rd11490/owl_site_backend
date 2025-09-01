import pytest
import pandas as pd
import json
from handlers.get_setup import get_setup

class DummyContext:
    pass

def make_event(query_params=None):
    return {'queryStringParameters': query_params}

def test_default_season(monkeypatch):
    # Patch pd.read_csv to return test DataFrames
    test_players = pd.DataFrame({'teamName': ['TeamA'], 'player': ['Player1']})
    test_comps = pd.DataFrame({'comp': ['Comp1']})
    test_stats = pd.DataFrame({'Stat': ['Stat1']})
    test_stages = pd.DataFrame({'Stage': ['Stage1']})
    test_map_types = pd.DataFrame({'Map Type': ['Type1']})
    test_map_names = pd.DataFrame({'Map Name': ['Map1']})
    test_heroes = pd.DataFrame({'Hero': ['Hero1']})
    monkeypatch.setattr(pd, 'read_csv', lambda path: {
        'teams_players.csv': test_players,
        'comps_list.csv': test_comps,
        'stats.csv': test_stats,
        'stage.csv': test_stages,
        'map_types.csv': test_map_types,
        'map_names.csv': test_map_names,
        'heroes.csv': test_heroes
    }[path.split('/')[-1]])
    event = make_event()
    result = get_setup(event, DummyContext())
    assert result['statusCode'] == 200
    body = json.loads(result['body'])
    assert 'comps' in body
    assert 'heroes' in body
    assert 'mapNames' in body
    assert 'mapTypes' in body
    assert 'players' in body
    assert 'stats' in body
    assert 'stages' in body
    assert 'teams' in body

def test_season_tag(monkeypatch):
    monkeypatch.setattr(pd.DataFrame, 'to_csv', lambda *args, **kwargs: None)
    # Patch pd.read_csv to return all expected DataFrames for a season
    test_players = pd.DataFrame({'teamName': ['TeamB'], 'player': ['Player2']})
    test_stats = pd.DataFrame({'Stat': ['Stat1']})
    test_stages = pd.DataFrame({'Stage': ['Stage1']})
    test_comps = pd.DataFrame({'comp': ['Comp1']})
    test_map_types = pd.DataFrame({'Map Type': ['Type1']})
    test_map_names = pd.DataFrame({'Map Name': ['Map1']})
    test_heroes = pd.DataFrame({'Hero': ['Hero1']})
    def mock_read_csv(path):
        fname = path.split('/')[-1]
        if 'players' in fname:
            return test_players
        elif 'stats' in fname:
            return test_stats
        elif 'stage' in fname:
            return test_stages
        elif 'comps' in fname:
            return test_comps
        elif 'map_types' in fname:
            return test_map_types
        elif 'map_names' in fname:
            return test_map_names
        elif 'heroes' in fname:
            return test_heroes
        else:
            return pd.DataFrame()
    monkeypatch.setattr(pd, 'read_csv', mock_read_csv)
    event = make_event({'season': '2018'})
    result = get_setup(event, DummyContext())
    body = json.loads(result['body'])
    assert 'players' in body
    assert body['players'][0]['teamName'] == 'TeamB'
