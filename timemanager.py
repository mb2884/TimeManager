#!/usr/bin/env python


# ----------------------------------------------------------------------
# timemanager.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# ----------------------------------------------------------------------


import datetime
import os
import flask
from flask import request, jsonify
import flask_talisman
import dbfuncs as database
import auth
import tasksplitter
import dotenv
from datetime import timedelta
from dateutil import parser


# ----------------------------------------------------------------------

app = flask.Flask(__name__, )

# Set the static folder
app.static_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static')


dotenv.load_dotenv()
app.secret_key = os.getenv('APP_SECRET_KEY')

flask_talisman.Talisman(app, content_security_policy=None)

# ----------------------------------------------------------------------


@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

# ----------------------------------------------------------------------


@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

# ----------------------------------------------------------------------


@app.route('/add-event', methods=['POST'])
def add_event():
    data = request.get_json()
    username = data.get('username')
    title = data.get('title')
    start = data.get('start')
    end = data.get('end')
    all_day = data.get('allDay')
    days_of_week = data.get('daysOfWeek')
    color = data.get('color')
    start_recur = data.get('startRecur')
    end_recur = data.get('endRecur')

    user_id = database.get_user_id(username)

    print("Adding event: ", username, title, start, end,
          all_day, color, days_of_week, start_recur, end_recur)
    event_id = database.addEvent(
        user_id, title, start, end, all_day, None, color, days_of_week, start_recur, end_recur)
    return jsonify({'id': event_id})

# ----------------------------------------------------------------------


@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.get_json()
    username = data.get('username')
    title = data.get('title')
    start = parser.parse(data.get('start')) - timedelta(hours=4)
    end = parser.parse(data.get('end')) - timedelta(hours=4)
    length = data.get('length')
    events = data.get('events')
    user_id = database.get_user_id(username)

    print("Adding task: ", username, title, start, end, length)

    task_id = database.addTask(user_id, title, start, end, length)
    try:
        tasksplitter.split_tasks(
            user_id, title, start, end, length, task_id, events)
    except Exception as ex:
        database.delete_task(task_id)
        return jsonify({'error': str(ex)}), 500
    return jsonify({'id': task_id})

# ----------------------------------------------------------------------


@app.route('/update-event', methods=['POST'])
def update_event():
    try:
        data = request.get_json()
        event_id = data.get('event_id')
        title = data.get('title')
        start = data.get('start')
        end = data.get('end')
        all_day = data.get('allDay')

        print("Updating event: ", event_id, title, start, end, all_day)
        # Update the event in the database
        database.update_event(event_id, title, start, end, all_day)

        return jsonify({'message': 'Event updated successfully'})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# ----------------------------------------------------------------------


@app.route('/save-settings', methods=['POST'])
def save_settings():
    try:
        data = request.get_json()
        username = data.get('username')
        earliest_time = data.get('earliestTime')
        latest_time = data.get('latestTime')
        ideal_chunk_size = data.get('idealChunkSize')
        event_padding = data.get('eventPadding')

        user_id = database.get_user_id(username)

        print("Saving settings: ", username, earliest_time, latest_time,
              ideal_chunk_size, event_padding)
        # Update the event in the database
        database.update_user_settings(
            user_id, earliest_time, latest_time, ideal_chunk_size, event_padding)

        return jsonify({'message': 'Settings saved successfully'})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# ----------------------------------------------------------------------


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

# ----------------------------------------------------------------------


@app.route('/delete-task', methods=['POST'])
def delete_task():
    try:
        data = request.get_json()
        task_id = data.get('task_id')

        # Implement the logic to delete the event from the database
        database.delete_task(task_id)

        # Return a success message to the client
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as ex:
        # If an error occurs, return an error message
        return jsonify({'error': str(ex)}), 500

# ----------------------------------------------------------------------


@app.route('/get-events', methods=['GET'])
def get_events():
    username = auth.authenticate()
    user_id = database.get_user_id(username)

    return flask.jsonify(database.getEvents(user_id))

# ----------------------------------------------------------------------


@app.route('/get-tasks', methods=['GET'])
def get_tasks():
    username = auth.authenticate()
    user_id = database.get_user_id(username)

    return flask.jsonify(database.getTasks(user_id))


# ----------------------------------------------------------------------


@app.route('/')
@app.route('/landing')
def landing():
    return flask.render_template('landing.html')

# ----------------------------------------------------------------------


@app.route('/index', methods=['GET'])
def index():
    username = auth.authenticate()
    work_start_time, work_end_time, ideal_chunk_length, event_padding = database.get_user_settings(
        database.get_user_id(username))
    html_code = flask.render_template('index.html',
                                      username=username,
                                      work_start_time=work_start_time,
                                      work_end_time=work_end_time,
                                      ideal_chunk_length=ideal_chunk_length,
                                      event_padding=event_padding)
    response = flask.make_response(html_code)
    return response


# ----------------------------------------------------------------------

# Will create a new test user in the database and simulate several events and tasks
def main():
    # Create a new test user
    user_id = database.get_user_id('test')
    database.delete_all(user_id)
    user_id = database.get_user_id('test')

    # Add the event to the database: mb2884 LIN250 Lecture 1/30/2024, 1:30:00 PM 1/30/2024, 2:50:00 PM False #324191 [2, 4] 1/30/2024, 1:30:00 PM 2024-04-27
    linid = database.addEvent(user_id, 'LIN250 Lecture', '2024-01-30T13:30:00', '2024-01-30T14:50:00',
                              False, None, '#324191', [2, 4], '2024-01-30T13:30:00', '2024-04-27')

    # Add the event to the database: 6 COS333 Lecture 1/30/2024, 3:00:00 PM 1/30/2024, 4:20:00 PM False None #096636 [2, 4] 1/30/2024, 3:00:00 PM 2024-04-27
    coslecid = database.addEvent(user_id, 'COS333 Lecture', '2024-01-30T15:00:00', '2024-01-30T16:20:00',
                                 False, None, '#096636', [2, 4], '2024-01-30T15:00:00', '2024-04-27')

    # Add the event to the database: 6 JPN306 1/31/2024, 3:00:00 PM 1/31/2024, 4:20:00 PM False None #721d88 [3, 5] 1/31/2024, 3:00:00 PM 2024-04-27
    jpnid = database.addEvent(user_id, 'JPN306', '2024-01-31T15:00:00', '2024-01-31T16:20:00',
                              False, None, '#721d88', [3, 5], '2024-01-31T15:00:00', '2024-04-27')

    # Add the event to the database: 6 COS IW 09: OS 2/1/2024, 11:00:00 AM 2/1/2024, 12:20:00 PM False None #886606 [4] 2/1/2024, 11:00:00 AM 2024-04-27
    iwid = database.addEvent(user_id, 'COS IW 09: OS', '2024-02-01T11:00:00', '2024-02-01T12:20:00',
                             False, None, '#886606', [4], '2024-02-01T11:00:00', '2024-04-27')

    # Add the event to the database: 6 COS IW Getting Started Meeting 1/30/2024, 4:30:00 PM 1/30/2024, 5:15:00 PM False None #886606 [] 1/30/2024, 4:30:00 PM
    iwmeetingid = database.addEvent(user_id, 'COS IW Getting Started Meeting', '2024-01-30T16:30:00', '2024-01-30T17:15:00',
                                    False, None, '#886606', [], '2024-01-30T16:30:00', None)

    # Add the event to the database: 6 Moose Mondays 1/29/2024, 8:00:00 PM 1/29/2024, 9:00:00 PM False None #027cb7 [] 1/29/2024, 8:00:00 PM
    mooseid = database.addEvent(user_id, 'Moose Mondays', '2024-01-29T20:00:00', '2024-01-29T21:00:00',
                                False, None, '#027cb7', [], '2024-01-29T20:00:00', None)

    # Update the event to the database: 21 Moose Mondays 2024-01-29T20:00:00.000Z 2024-01-29T22:00:00.000Z False
    database.update_event(mooseid, 'Moose Mondays',
                          '2024-01-29T20:00:00', '2024-01-29T22:00:00', False)

    # Moving the event to the database: 21 Moose Mondays 2024-01-30T18:30:00.000Z 2024-01-30T20:30:00.000Z False
    database.update_event(mooseid, 'Moose Mondays',
                          '2024-01-30T18:30:00', '2024-01-30T20:30:00', False)

    # Add the event to the database: 6 temp 2024-01-31T17:00:00.000Z 2024-01-31T18:00:00.000Z False None None None None None
    tempid = database.addEvent(user_id, 'temp', '2024-01-31T17:00:00', '2024-01-31T18:00:00',
                               False, None, None, None, None, None)

    # Delete the event from the database: 21 temp
    database.delete_event(tempid)

    # Update user settings in the database: mb2884 10:00:00 23:59:00 60 10
    database.update_user_settings(user_id, '10:00:00', '23:59:00', 60, 10)

    # Add the task to the database: mb2884 First Pset 2024-01-30 11:00:00+00:00 2024-02-03 00:59:00+00:00 3
    psetid = database.addTask(user_id, 'First Pset',
                              '2024-01-30T11:00:00', '2024-02-03T00:59:00', 3)

    # Add the task to the database: mb2884 First Essay 2024-01-29 12:00:00+00:00 2024-02-06 00:59:00+00:00 10
    essayid = database.addTask(
        user_id, 'First Essay', '2024-01-29T12:00:00', '2024-02-06T00:59:00', 10)

    # Delete the task from the database: psetid
    database.delete_task(psetid)

    print("events: ", database.getEvents(user_id))
    print("tasks: ", database.getTasks(user_id))
    print("settings: ", database.get_user_settings(user_id))
    print("Testing error handling...")

    try:
        database.get_user_id(None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "Username cannot be None", "Error message is incorrect"
    try:
        database.get_user_settings(None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "User ID cannot be None", "Error message is incorrect"
    try:
        database.getEvents(None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "User ID cannot be None", "Error message is incorrect"
    try:
        database.getTasks(None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "User ID cannot be None", "Error message is incorrect"
    try:
        database.addEvent(None, None, None, None, None,
                          None, None, None, None, None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "One or more arguments are None", "Error message is incorrect"
    try:
        database.addTask(None, None, None, None, None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "One or more arguments are None", "Error message is incorrect"
    try:
        database.delete_event(None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "Event ID cannot be None", "Error message is incorrect"
    try:
        database.delete_task(None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "Task ID cannot be None", "Error message is incorrect"
    try:
        database.delete_all(None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "User ID cannot be None", "Error message is incorrect"
    try:
        database.update_event(None, None, None, None, None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "One or more arguments are None", "Error message is incorrect"
    try:
        database.update_user_settings(None, None, None, None, None)
    except Exception as ex:
        print("Error: ", ex)
        assert str(ex) == "One or more arguments are None", "Error message is incorrect"

    print("All tests complete!")


if __name__ == '__main__':
    main()
    
