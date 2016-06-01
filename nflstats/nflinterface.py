import nflanalyze
import nfldb
import psycopg2

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import json

app = Flask(__name__)



@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/get_player_from_id', methods=['POST'])
def get_player_from_id():
    payload = json.loads(request.data)
    id = payload['id']
    player = nflanalyze.get_player_from_id(id)
    return to_json(player)

@app.route('/get_player', methods=['POST'])
def get_player():
    payload = json.loads(request.data)
    last_name = payload['last_name']
    first_name = payload['first_name']
    team = payload['team']
    player = nflanalyze.get_player(last_name, first_name, team)
    if player == None:
        return nflanalyze.to_json({'message': 'not found'})
    return to_json(player)

@app.route('/get_player_all_time_stats', methods=['POST'])
def get_player_all_time_stats():
    payload = json.loads(request.data)
    id = payload['id']
    stats = nflanalyze.get_player_all_time_stats(id)
    if stats == None:
        return nflanalyze.to_json({'message': 'not found'})
    return to_json(stats)

@app.route('/get_team_roster', methods=['POST'])
def get_team_roster():
    payload = json.loads(request.data)
    team = payload['team']
    roster = nflanalyze.get_team_roster(team)
    return to_json(roster)

@app.route('/get_player_stats_for_year', methods=['POST'])
def get_player_stats_for_year():
    payload = json.loads(request.data)
    last_name = payload['last_name']
    first_name = payload['first_name']
    team = payload['team']
    year = payload['year']
    stats = nflanalyze.get_player_stats_for_year(last_name, first_name, team, year)
    if stats == None:
        return nflanalyze.to_json({'message': 'not found'})
    return to_json(stats)

@app.route('/get_player_all_time_stats_by_year', methods=['POST'])
def get_player_all_time_stats_by_year():
    payload = json.loads(request.data)
    id = payload['id']
    years = nflanalyze.get_player_all_time_stats_by_year(id)
    if years == None:
        return nflanalyze.to_json({'message': 'not found'})
    return to_json(years)

@app.route('/fuzzy_player_search', methods=['POST'])
def fuzzy_player_search():
    payload = json.loads(request.data)
    name = payload['name']
    players = nflanalyze.fuzzy_search(name)
    return to_json(players)

@app.route('/get_all_names', methods=['POST'])
def get_all_names():
    names = nflanalyze.get_all_names()
    names = [{'name': '%s, %s, %s' % (name['full_name'], name['position'], name['team']), 'id': name['player_id']} for name in names]
    return to_json(names)

def to_json(obj):
    return json.dumps(extract_fields(obj))

def extract_fields(obj):
    if type(obj) is list:
        for i,o in enumerate(obj):
            if type(o) is nfldb.types.Player:
                obj[i] = convert_player(o)
            elif type(o) is tuple:
                obj[i] = convert_player(o[0])
            elif type(o) is psycopg2.extras.RealDictRow:
                continue
            elif type(o) is str:
                continue
            elif type(o) is dict:
                continue
            else:
                obj[i] = dict((f, getattr(o, f)) for f in o.fields)
                for k,v in vars(o).iteritems():
                    obj[i][k] = v
    else:
        if type(obj) is nfldb.types.Player:
            obj = convert_player(obj)
        else:
            obj = dict((f, str(obj[f])) for f in obj)
    return obj

def convert_player(player):
    obj = dict((f, getattr(player, f)) for f in player.sql_fields() if getattr(player, f) != None)
    obj['position'] = str(getattr(player, 'position'))
    obj['status'] = str(getattr(player, 'status'))
    return obj

if __name__ == "__main__":
    app.run()
