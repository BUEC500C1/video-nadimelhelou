# Nadim El Helou - EC 500 C1 - HW4 Twitter Video API

# References: 
# 

import flask
from flask import request, jsonify
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Twitter Video API</h1><p>This API returns a video with a given user's tweets. By Nadim El Helou</p>"


@app.route('/tweets', methods=['GET'])
def api_id():
    # Check if a username was given
    if 'username' in request.args:
        username = request.args['username']
    else:
        return "Error: No username provided. Please enter a twitter username."
    
    return "Twitter handle: " + username


app.run()

