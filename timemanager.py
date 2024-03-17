#!/usr/bin/env python

#-----------------------------------------------------------------------
# timemanager.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
#-----------------------------------------------------------------------

import os
import time
import flask
import database
import auth

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------

# Routes for authentication.

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    username = auth.authenticate()

    html_code = flask.render_template('index.html', username=username)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
