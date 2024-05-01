#!/usr/bin/env python


# ----------------------------------------------------------------------
# timemanager.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# ----------------------------------------------------------------------


import os
import flask
from flask import request, jsonify
# import flask_wtf.csrf
# import flask_talisman
import dbfuncs as database
import auth
import tasksplitter
import dotenv
from datetime import datetime, timedelta
from dateutil import parser


# ----------------------------------------------------------------------


app = flask.Flask(__name__, )




# Set the static folder
app.static_folder = os.path.join(
   os.path.dirname(os.path.abspath(__file__)), 'static')


dotenv.load_dotenv()
app.secret_key = os.getenv('APP_SECRET_KEY')


# flask_wtf.csrf.CSRFProtect(app)
# flask_talisman.Talisman(app, content_security_policy=None)


# ----------------------------------------------------------------------


# Routes for authentication.


@app.route('/logoutapp', methods=['GET'])
def logoutapp():
   return auth.logoutapp()


@app.route('/logoutcas', methods=['GET'])
def logoutcas():
   return auth.logoutcas()


#@app.route('/logout')
#def logout():
##   logout_url = 'https://fed.princeton.edu/cas/logout'
#    service_url = urllib.parse.quote(request.url_root + 'logout')
#    redirect_url = logout_url + '?service=' + service_url
#    return redirect(redirect_url)




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
   
   print("Adding event: ", username, title, start, end, all_day, color, days_of_week, start_recur, end_recur)
   event_id = database.addEvent(user_id, title, start, end, all_day, None, color, days_of_week, start_recur, end_recur)
   return jsonify({'id': event_id})


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
       tasksplitter.split_tasks(user_id, title, start, end, length, task_id, events)
   except Exception as ex:
         database.delete_task(task_id)
         return jsonify({'error': str(ex)}), 500
   return jsonify({'id': task_id})


@app.route('/update-event', methods=['POST'])
def update_event():
   try:
       data = request.get_json()
       event_id = data.get('event_id')
       title = data.get('title')
       start = data.get('start')
       end = data.get('end')
       all_day = data.get('allDay')
      
       # Update the event in the database
       database.update_event(event_id, title, start, end, all_day)
      
       return jsonify({'message': 'Event updated successfully'})
   except Exception as ex:
       return jsonify({'error': str(ex)}), 500
   
   
@app.route('/save-settings', methods=['POST'])
def save_settings():
   try:
       data = request.get_json()
       username = data.get('username')
       earliest_time = data.get('earliestTime')
       latest_time = data.get('latestTime')
       ideal_chunk_size = data.get('idealChunkSize')
       event_padding = data.get('eventPadding')
      
       # Update the event in the database
       database.update_user_settings(username, earliest_time, latest_time, ideal_chunk_size, event_padding)
      
       return jsonify({'message': 'Settings saved successfully'})
   except Exception as ex:
       return jsonify({'error': str(ex)}), 500


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


@app.route('/delete-task', methods=['POST'])
def delete_task():
   try:
       data = request.get_json()
       task_id = data.get('task_id')
       print("reported task_id: ", task_id)


       # Implement the logic to delete the event from the database
       database.delete_task(task_id)


       # Return a success message to the client
       return jsonify({'message': 'Task deleted successfully'})
   except Exception as ex:
       # If an error occurs, return an error message
       return jsonify({'error': str(ex)}), 500


@app.route('/get-events', methods=['GET'])
def get_events():
   username = auth.authenticate()
   user_id = database.get_user_id(username)
  
   return flask.jsonify(database.getEvents(user_id))


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


@app.route('/index', methods=['GET'])
def index():
   username = auth.authenticate()
   work_start_time, work_end_time, ideal_chunk_length, event_padding = database.get_user_settings(database.get_user_id(username))
   html_code = flask.render_template('index.html',
                                     username=username,
                                     work_start_time=work_start_time,
                                     work_end_time=work_end_time,
                                     ideal_chunk_length=ideal_chunk_length,
                                     event_padding=event_padding)
   response = flask.make_response(html_code)
   print(database.getEvents(database.get_user_id(username)))
   return response


# ----------------------------------------------------------------------


if __name__ == '__main__':
   app.run(debug=True)

