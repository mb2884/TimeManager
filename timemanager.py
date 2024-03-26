#!/usr/bin/env python

#-----------------------------------------------------------------------
# timemanager.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
#-----------------------------------------------------------------------

import os
import flask
#import database
import auth
from datetime import datetime, timedelta

#-----------------------------------------------------------------------

app = flask.Flask(__name__, )

# Set the static folder
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

os.environ['APP_SECRET_KEY'] = 'secretkey'
app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------

def generate_time_slots(start_time, end_time):
    # Convert start and end time strings to datetime objects
    start = datetime.strptime(start_time, "%I %p")
    end = datetime.strptime(end_time, "%I %p")

    # Initialize the list of time slots
    time_slots = []

    # Generate time slots at 1-hour intervals
    current_time = start
    while current_time <= end:
        time_slots.append(current_time.strftime("%I %p"))
        current_time += timedelta(hours=1)

    return time_slots

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
    # Sample events data (replace with your own events data)
    events = [
        {"title": "Event 1", "start_time": "09:00 AM", "end_time": "11:00 AM", "day": "Monday"},
        {"title": "Event 2", "start_time": "02:00 PM", "end_time": "04:00 PM", "day": "Tuesday"},
        {"title": "Event 3", "start_time": "10:00 AM", "end_time": "12:00 PM", "day": "Wednesday"}
        # Add more events as needed
    ]

    # Generate time markers
    time_markers = [f'{hour % 12 or 12}:00 {["AM", "PM"][hour // 12]}' for hour in range(0, 24)]
    
    html_code = flask.render_template('index.html', 
                                      username=username,
                                      time_markers=time_markers,
                                      events=events)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
