#!/usr/bin/env python

#-----------------------------------------------------------------------
# timemanager.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
#-----------------------------------------------------------------------

import os
import flask
import dbfuncs as database
# import auth

#-----------------------------------------------------------------------

app = flask.Flask(__name__, )

# Set the static folder
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

os.environ['APP_SECRET_KEY'] = 'secretkey'
app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------

# Routes for authentication.

# @app.route('/logoutapp', methods=['GET'])
# def logoutapp():
#     return auth.logoutapp()

# @app.route('/logoutcas', methods=['GET'])
# def logoutcas():
#     return auth.logoutcas()

#-----------------------------------------------------------------------
@app.route('/add-event', methods=['GET'])
def events():
    title = flask.request.args.get('title')
    start = flask.request.args.get('start')
    end = flask.request.args.get('end')
    all_day = flask.request.args.get('allDay')
    database.addEvent(title, start, end, all_day)
    print(database.getEvents())
    
    return

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    # username = auth.authenticate()
    # Sample events data (replace with your own events data)
    
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
