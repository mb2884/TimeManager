#!/usr/bin/env python

# -----------------------------------------------------------------------
# timemanager.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# -----------------------------------------------------------------------

import os
import flask
from flask import request, jsonify
import dbfuncs as database
# import auth

# -----------------------------------------------------------------------

app = flask.Flask(__name__, )

# Set the static folder
app.static_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static')

os.environ['APP_SECRET_KEY'] = 'secretkey'
app.secret_key = os.environ['APP_SECRET_KEY']

# -----------------------------------------------------------------------

# Routes for authentication.

# @app.route('/logoutapp', methods=['GET'])
# def logoutapp():
#     return auth.logoutapp()

# @app.route('/logoutcas', methods=['GET'])
# def logoutcas():
#     return auth.logoutcas()

# -----------------------------------------------------------------------


@app.route('/add-event', methods=['POST'])
def add_event():
    data = request.get_json()
    title = data.get('title')
    start = data.get('start')
    end = data.get('end')
    all_day = data.get('allDay')
    event_id = database.addEvent(title, start, end, all_day)
    return jsonify({'id': event_id})


@app.route('/delete-event', methods=['POST'])
def delete_event():
    try:
        # Get the event ID from the request
        data = request.get_json()
        event_id = data.get('event_id')

        # Implement the logic to delete the event from the database
        database.delete_event(event_id)

        # Return a success message to the client
        return jsonify({'message': 'Event deleted successfully'})
    except Exception as ex:
        # If an error occurs, return an error message
        return jsonify({'error': str(ex)}), 500


@app.route('/get-events', methods=['GET'])
def get_events():
    return flask.jsonify(database.getEvents())


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    # username = auth.authenticate()
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

# -----------------------------------------------------------------------
