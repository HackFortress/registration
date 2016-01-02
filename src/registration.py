#!/usr/bin/env python

import json
import re

import database

# import flask stuff
from flask import Flask
from flask import Response
from flask import request
from flask import render_template
from flask import make_response

app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
	data = {}
	data["player_times"] = get_player_times
	return render_template("index.html")

@app.route("/newteam")
def newteam():
	data = {}
	data["player_times"] = get_player_times
	return render_template("newteam.html")

@app.route("/register_team", methods=["POST"])
def register_team():
	try:
		team_name=request.json['name']
		team_exists=database_connection.search_team(team_name)

		if team_exists > 0:
			return json.dumps({ "message": "Team Name Already in Use", 'code': 101 }), 500


		team=database.Team(team_name)
		team_id=database_connection.add_record(team)

		for each_form in request.json['members']:
			for each_user in request.json['members'][each_form]:
				userData=request.json['members'][each_form][each_user]

				if userData['handle'] != '':
					if each_form=='tf2':
						type_player=2
					else:
						type_player=1
					
					print team_name,userData['handle'], userData['phone'], userData['email'],type_player
					team_member=database.TeamMember(userData['handle'],userData['email'],userData['phone'],team_id,type_player)
					database_connection.add_record(team_member)
	except:
		return json.dumps({ "message": "An Error Has Occurred", 'code': 100 }), 500

	return json.dumps({"message": "Welcome to Hack Fortress!"}), 200

def get_team_times():
	return [10, 11, 12, 1]

def get_player_times():
	return [10, 11, 12, 1]

if __name__ == "__main__":
	database_connection=database.Database('hf.db')
	app.run(host="0.0.0.0", port=4000, debug=True)	