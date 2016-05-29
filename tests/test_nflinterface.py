from context import nflinterface

import pytest
import tempfile
from flask import json


@pytest.fixture
def client(request):
    nflinterface.app.config['TESTING'] = True
    client = nflinterface.app.test_client()
    return client

def test_app():
    assert nflinterface.app != None

def test_home(client):
    response = client.get('/', follow_redirects=True)
    assert b'nflstats' in response.data

def test_get_player(client):
    payload = {
        'last_name':'Brees',
        'first_name':'Drew',
        'team':'NO'}
    response = client.post('/get_player', data=json.dumps(payload))
    json_data = json.loads(response.data)
    assert json_data['position'] == 'QB'
    assert json_data['status'] == 'Active'
    assert json_data['full_name'] == 'Drew Brees'

def test_get_player_all_time_stats(client):
    payload = {
        'last_name':'Manning',
        'first_name':'Eli',
        'team':'NYG'}
    response = client.post('/get_player_all_time_stats', data=json.dumps(payload))
    json_data = json.loads(response.data)
    assert json_data[0]['passing_tds'] == 205

def test_get_player_stats_for_year(client):
    payload = {
        'last_name':'Manning',
        'first_name':'Eli',
        'team':'NYG',
        'year': 2015}
    response = client.post('/get_player_stats_for_year', data=json.dumps(payload))
    json_data = json.loads(response.data)
    assert json_data[0]['passing_tds'] == 35

def test_get_player_all_time_stats_by_year(client):
    payload = {
        'last_name':'Manning',
        'first_name':'Eli',
        'team':'NYG'}
    response = client.post('/get_player_all_time_stats_by_year', data=json.dumps(payload))
    json_data = json.loads(response.data)
    assert json_data[6]['passing_tds'] == 35
    assert json_data[6]['year'] == 2015

def test_get_team_roster(client):
    payload = {
        'team': 'NO'
    }
    response = client.post('/get_team_roster', data=json.dumps(payload))
    roster = json.loads(response.data)
    assert roster[0]['team'] == 'NO'
    assert roster[0]['status'] == 'Active'

def test_fuzzy_player_search(client):
    payload = {
        'name': 'peyton Mannz'
    }
    response = client.post('/fuzzy_player_search', data=json.dumps(payload))
    players = json.loads(response.data)
    assert players[0]['full_name'] == 'Peyton Manning'

def test_get_all_names(client):
    response = client.post('/get_all_names')
    names = json.loads(response.data)
    assert len(names) == 6510
