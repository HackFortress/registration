#!/usr/bin/env python

import json

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

@app.route("/register_team", methods=["POST"])
def register_team():
    print request.form

def get_team_times():
    return [10, 11, 12, 1]

def get_player_times():
    return [10, 11, 12, 1]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
