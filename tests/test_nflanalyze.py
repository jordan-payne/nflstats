from context import nflanalyze
import json

def test_get_team():
    team = nflanalyze.get_team('ARI')
    assert team['team_id'] == 'ARI'
    assert team['city'] == 'Arizona'
    assert team['name'] == 'Cardinals'

def test_get_stats_categories():
    assert len(nflanalyze.get_stats_categories()) == 109

def test_get_all_teams():
    assert len(nflanalyze.get_all_teams()) == 33

def test_fuzzy_search():
    (player, dist) = nflanalyze.fuzzy_search('eli manni')
    assert player.first_name == 'Eli'
    assert player.last_name == 'Manning'

def test_get_player():
    first_name = 'Peyton'
    last_name = 'Manning'
    team = 'UNK'
    player = nflanalyze.get_player(last_name, first_name, team)
    assert player['first_name'] == first_name
    assert player['last_name'] == last_name
    assert player['team'] == team

def test_get_player_all_time_stats():
    first_name = 'Peyton'
    last_name = 'Manning'
    team = 'UNK'
    stats = nflanalyze.get_player_all_time_stats(last_name, first_name, team)
    assert getattr(stats[0], 'passing_att') == 3815
    assert getattr(stats[0], 'rushing_att') == 129
    assert getattr(stats[0], 'passing_yds') == 29053

def test_get_player_stats_for_year():
    first_name = 'Eli'
    last_name = 'Manning'
    team = 'NYG'
    year = 2015
    stats = nflanalyze.get_player_stats_for_year(last_name, first_name, team, year)
    assert getattr(stats[0], 'offense_tds') == 35
    assert getattr(stats[0], 'passing_int') == 14

def test_get_player_all_time_stats_by_year():
    first_name = 'Eli'
    last_name = 'Manning'
    team = 'NYG'
    years = nflanalyze.get_player_all_time_stats_by_year(last_name, first_name, team)
    assert len(years) == 7
    assert getattr(years[6], 'offense_tds') == 35

def test_get_team_roster():
    team = 'NO'
    players = nflanalyze.get_team_roster(team)
    assert players[0].team == 'NO'
    assert str(players[0].status) == 'Active'

def test_fuzzy_search():
    name = 'peyton Mannz'
    players = nflanalyze.fuzzy_search(name)
    assert players[0][0].full_name == 'Peyton Manning'

def test_get_player_from_id():
    id = '00-0027685'
    player = nflanalyze.get_player_from_id(id)
    assert player.first_name == 'Emmanuel'

def test_get_all_names():
    names = nflanalyze.get_all_names()
    assert len(names) == 6510
