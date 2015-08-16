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
	player={'hack':{},'tf2':{}}
	team_name=None
	for each_form in request.form:
		if each_form == 'team-name':
			team_name=request.form[each_form]
		else:
			player_object=re.match('(?P<player_type>^\S{3,4})_(?P<input_type>\S*)_(?P<number>\d{1,3}$)',each_form)
			
			if player_object:
				try:
					player_type=player_object.group('player_type')
					input_type=player_object.group('input_type')
					player_number=player_object.group('number')

					if player_number not in player[player_type]:
						player[player_type][player_number]={}

					player[player_type][player_number][input_type]=request.form[each_form]
				except:
					raise
					next
	if team_name is not None:
		team=database.Team(team_name)
		team_id=database_connection.add_record(team)

		if team_id == -1:
			print "Error Adding Team"
		else:
			for each_type in player:
				for each_player in player[each_type]:
					try:
						if each_type=='tf2':
							type_player=2
						else:
							type_player=1
						handle=player[each_type][each_player]['handle']
						phone=player[each_type][each_player]['phone']
						email=player[each_type][each_player]['email']

						team_member=database.TeamMember(handle,phone,email,team_id,type_player)
						database_connection.add_record(team_member)
					except:
						raise
						next
	
	return "ok"

def get_team_times():
	return [10, 11, 12, 1]

def get_player_times():
	return [10, 11, 12, 1]

if __name__ == "__main__":
	database_connection=database.Database('/tmp/hf.db')
	app.run(host="0.0.0.0", port=4000, debug=True)
	