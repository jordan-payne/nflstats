import nflanalyze
import nfldb

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
    last_name = payload['last_name']
    first_name = payload['first_name']
    team = payload['team']
    stats = nflanalyze.get_player_all_time_stats(last_name, first_name, team)
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
    last_name = payload['last_name']
    first_name = payload['first_name']
    team = payload['team']
    years = nflanalyze.get_player_all_time_stats_by_year(last_name, first_name, team)
    if years == None:
        return nflanalyze.to_json({'message': 'not found'})
    return to_json(years)

def to_json(obj):
    return json.dumps(extract_fields(obj))

def extract_fields(obj):
    if type(obj) is list:
        for i,o in enumerate(obj):
            if type(o) is nfldb.types.Player:
                obj[i] = dict((f, str(getattr(o, f))) for f in o.sql_fields())
            else:
                obj[i] = dict((f, str(getattr(o, f))) for f in o.fields)
                for k,v in vars(o).iteritems():
                    obj[i][k] = str(v)
    else:
        obj = dict((f, str(obj[f])) for f in obj)
    return obj

if __name__ == "__main__":
    app.run()
