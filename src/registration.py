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
from flask.ext.basicauth import BasicAuth

app = Flask(__name__, static_url_path='')

app.config['BASIC_AUTH_USERNAME'] = 'hfadmin'
app.config['BASIC_AUTH_PASSWORD'] = 'hfadmin'

basic_auth = BasicAuth(app)

@app.route("/")
def newteam():
	data = {}
	return render_template("newteam.html")

@app.route("/admin")
@basic_auth.required
def admin():
	tf2=[]
	hack=[]

	teamNames=database_connection.list_teams()
	
	if len(teamNames) > 0:
		members=database_connection.team_members(teamNames[0])
		if 'tf2' in members:
			tf2=members['tf2']
		if 'hack' in members:
			hack=members['hack']
	for x in range(len(tf2),6):
		tf2.append({'name':'','email':'','phone':'','teamid':'','membertype':'','id':'-1'})
	for x in range(len(hack),4):
		hack.append({'name':'','email':'','phone':'','teamid':'','membertype':'','id':'-1'})

	return render_template("admin.html",teamNames=teamNames,hack=hack,tf2=tf2)
@app.route("/view_team", methods=["POST"])
@basic_auth.required
def view():
	team=request.json['team']
	members=None
	hack=[]
	tf2=[]

	if team is not None:
		members=database_connection.team_members(team)
	else:
		message="No team set"
		return json.dumps({ "message": message, 'code': 102 }), 500
	if members is not None:
		if 'tf2' in members:
			tf2=members['tf2']
		if 'hack' in members:
			hack=members['hack']
		for x in range(len(tf2),6):
			tf2.append({'name':'','email':'','phone':'','teamid':'','membertype':'','id':'-1'})
		for x in range(len(hack),4):
			hack.append({'name':'','email':'','phone':'','teamid':'','membertype':'','id':'-1'})

		return json.dumps({'hack':hack,'tf2':tf2})
	else:
		message="No team members for team {0}".format(team)
		return json.dumps({ "message": message, 'code': 103 }), 500

@app.route("/update_team", methods=["POST"])
@basic_auth.required
def update():
	if 'team' in request.json:
		teamName=request.json['team']
		if 'hack' in request.json:
			for eachMember in request.json['hack']:
				if int(eachMember['id']) >=0:
					database_connection.updateMember(eachMember['id'],eachMember['handle'],eachMember['phone'],eachMember['email'])
				else:
					database_connection.addTeamMember(teamName,eachMember['handle'],eachMember['phone'],eachMember['email'],'hack')
		if 'tf2' in request.json:
			for eachMember in request.json['tf2']:
				if int(eachMember['id']) >=0:
					print eachMember
					database_connection.updateMember(eachMember['id'],eachMember['handle'],eachMember['phone'],eachMember['email'])
				else:
					database_connection.addTeamMember(teamName,eachMember['handle'],eachMember['phone'],eachMember['email'],'tf2')
	return json.dumps({'message':'Success'})

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
					
					team_member=database.TeamMember(userData['handle'],userData['email'],userData['phone'],team_id,type_player)
					database_connection.add_record(team_member)
	except:
		return json.dumps({ "message": "An Error Has Occurred", 'code': 100 }), 500

	return json.dumps({"message": "Welcome to Hack Fortress!"}), 200

if __name__ == "__main__":
	database_connection=database.Database('hf.db')
	app.run(host="0.0.0.0", port=4000)