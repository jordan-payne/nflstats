import nfldb, nfldbc, nflgame
import json

dbc = nfldbc.dbc

def get_team(team_name):
    with nfldb.Tx(dbc) as cursor:
        cursor.execute('SELECT * FROM team WHERE team_id = %s', [team_name,])
        return cursor.fetchone()

def get_all_teams():
    with nfldb.Tx(dbc) as cursor:
        cursor.execute('SELECT * FROM team;')
        return cursor.fetchall()

def get_stats_categories():
    return nfldb.stat_categories

def fuzzy_search(name, limit=1, team=None, position=None):
    return nfldb.player_search(dbc, name, limit=limit, team=team, position=position)

def get_player(last_name, first_name, team):
    with nfldb.Tx(dbc) as cursor:
        cursor.execute(
            '''SELECT * FROM player WHERE last_name = %s AND first_name = %s AND team = %s''',
            [last_name, first_name, team])
        player = cursor.fetchone()
        if player == None:
            team = 'UNK'
            cursor.execute(
                '''SELECT * FROM player WHERE last_name = %s AND first_name = %s AND team = %s''',
                [last_name, first_name, team])
            return cursor.fetchone()
        else:
            return player

def get_player_all_time_stats(last_name, first_name, team):
    player = get_player(last_name, first_name, team)
    q = nfldb.Query(dbc)
    # Only have 2009 onwards :(
    q.game(season_year=range(2009, 2016), season_type=['Regular', 'Postseason'])
    q.play_player(player_id=player['player_id'])
    return q.limit(1).as_aggregate()

def get_player_stats_for_year(last_name, first_name, team, year):
    player = get_player(last_name, first_name, team)
    q = nfldb.Query(dbc)
    q.game(season_year=year, season_type=['Regular', 'Postseason'])
    q.play_player(player_id=player['player_id'])
    return q.limit(1).as_aggregate()

def get_player_all_time_stats_by_year(last_name, first_name, team):
    player = get_player(last_name, first_name, team)
    results = []
    for year in range(2009, 2016):
        q = nfldb.Query(dbc)
        q.game(season_year=year, season_type=['Regular', 'Postseason'])
        q.play_player(player_id=player['player_id'])
        try:
            result = q.limit(1).as_aggregate()[0]
        except IndexError:
            continue
        else:
            result.year = year
            results.append(result)
    return results

def get_team_roster(team):
    q = nfldb.Query(dbc)
    players = q.player(team=team, status='Active').as_players()
    return players
