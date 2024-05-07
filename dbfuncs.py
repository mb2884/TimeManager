#!/usr/bin/env python

# ----------------------------------------------------------------------
# dbfuncs.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# ----------------------------------------------------------------------

import os
import sys
import sqlalchemy
import sqlalchemy.orm
import dotenv
import database
import pytz
import datetime

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
nytz = pytz.timezone('America/New_York')

# ----------------------------------------------------------------------


def get_user_id(username):
    assert username is not None, "Username cannot be None"
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Query the AppUser object from the database
            app_user = session.query(database.AppUser).filter_by(
                username=username).first()

            if app_user:
                return app_user.id
            else:
                # Create a new AppUser entry for the username
                new_user = database.AppUser(username=username)
                session.add(new_user)
                # Set default user settings
                new_user.earliest_time = datetime.time(8, 0)
                new_user.latest_time = datetime.time(22, 0)
                new_user.ideal_chunk_size = 120
                new_user.event_padding = 10
                session.commit()
                return new_user.id

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def get_user_settings(user_id):
    assert user_id is not None, "User ID cannot be None"
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Query the AppUser object from the database
            app_user = session.query(
                database.AppUser).filter_by(id=user_id).first()

            if app_user:
                return app_user.earliest_time, app_user.latest_time, app_user.ideal_chunk_size, app_user.event_padding
            else:
                return None

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def getEvents(user_id, filter_by_date=None):
    assert user_id is not None, "User ID cannot be None"
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:

            if filter_by_date:
                app_events = session.query(database.AppEvent).filter_by(user_id=user_id).filter(database.AppEvent.start_time >= filter_by_date[0]).filter(
                    database.AppEvent.end_time <= filter_by_date[1]).order_by(database.AppEvent.start_time).all()
            else:
                app_events = session.query(
                    database.AppEvent).filter_by(user_id=user_id).all()

            # Convert each AppEvent object into a dictionary
            event_dicts = []
            for event in app_events:
                days_of_week = []
                if event.days_of_week:
                    days_of_week = event.days_of_week.split(',')
                    days_of_week = [int(x) for x in days_of_week]
                if not days_of_week:
                    days_of_week = None
                    start_recur = None
                    end_recur = None
                    start_time = None
                    end_time = None
                else:
                    start_recur = event.start_recur.isoformat()
                    end_recur = event.end_recur.isoformat()
                    # Takes just the time from the datetime object
                    start_time = event.start_time.time().isoformat()
                    end_time = event.end_time.time().isoformat()

                event_dict = {
                    'title': event.title,
                    'start': event.start_time.isoformat(),  # Convert datetime to ISO format
                    'end': event.end_time.isoformat(),  # Convert datetime to ISO format
                    'allDay': event.all_day,
                    'id': event.id,
                    'parentTaskID': event.parent_task_id,
                    'color': event.color,
                    'daysOfWeek': days_of_week,
                    'startRecur': start_recur,
                    'endRecur': end_recur,
                    'startTime': start_time,
                    'endTime': end_time

                }
                event_dicts.append(event_dict)

        return event_dicts

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def getTasks(user_id):
    assert user_id is not None, "User ID cannot be None"
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Query all AppEvent objects from the database
            app_tasks = session.query(
                database.AppTask).filter_by(user_id=user_id).all()

            # Convert each AppEvent object into a dictionary
            task_dicts = []
            for task in app_tasks:
                task_dict = {
                    'title': task.title,
                    # Convert datetime to ISO format
                    'start': task.start_time.isoformat() if task.start_time else None,
                    # Convert datetime to ISO format
                    'end': task.due_date.isoformat() if task.due_date else None,
                    'length': task.est_length,
                    'id': task.id
                }
                task_dicts.append(task_dict)
        return task_dicts

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def addEvent(user_id, title, start_time, end_time, all_day, parent_task_id=None, color=None, days_of_week=None, start_recur=None, end_recur=None):
    assert user_id is not None, "User ID cannot be None"
    assert title is not None, "Title cannot be None"
    assert start_time is not None, "Start time cannot be None"
    assert end_time is not None, "End time cannot be None"
    assert all_day is not None, "All day cannot be None"
    print("Adding event with: ", user_id, title, start_time, end_time,
          all_day, parent_task_id, color, days_of_week, start_recur, end_recur)
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            if days_of_week:
                days_of_week = ','.join(str(x) for x in days_of_week)
            else:
                days_of_week = None
                start_recur = None
                end_recur = None
            print("Adding event with: ", user_id, title, start_time, end_time, all_day,
                  parent_task_id, color, days_of_week, start_recur, end_recur)
            app_event = database.AppEvent(
                user_id=user_id,
                title=title,
                start_time=start_time,
                end_time=end_time,
                all_day=all_day,
                parent_task_id=parent_task_id,
                color=color,
                days_of_week=days_of_week,
                start_recur=start_recur,
                end_recur=end_recur
            )
            session.add(app_event)
            session.commit()
            return app_event.id

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def addTask(user_id, title, start_time, due_date, est_length):
    assert user_id is not None, "User ID cannot be None"
    assert title is not None, "Title cannot be None"
    assert start_time is not None, "Start time cannot be None"
    assert due_date is not None, "Due date cannot be None"
    assert est_length is not None, "Estimated length cannot be None"
    print("Adding task with: ", user_id, title,
          start_time, due_date, est_length)
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            app_task = database.AppTask(
                user_id=user_id,
                title=title,
                start_time=start_time,
                due_date=due_date,
                est_length=est_length
            )
            session.add(app_task)
            session.commit()
            return app_task.id

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def delete_event(event_id):
    assert event_id is not None, "Event ID cannot be None"
    print(f"Deleting event with ID {event_id}...")
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Retrieve the event to be deleted
            event_to_delete = session.query(
                database.AppEvent).filter_by(id=event_id).first()

            if event_to_delete:
                # Delete the event
                session.delete(event_to_delete)
                session.commit()
                print(f"Event with ID {event_id} deleted successfully.")
            else:
                print(f"Event with ID {event_id} not found.")
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def delete_task(task_id):
    assert task_id is not None, "Task ID cannot be None"
    print(f"Deleting task with ID {task_id}...")
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Retrieve the event to be deleted
            task_to_delete = session.query(
                database.AppTask).filter_by(id=task_id).first()

            if task_to_delete:
                # Delete the event
                session.delete(task_to_delete)
                session.commit()
                print(f"Task with ID {task_id} deleted successfully.")
            else:
                print(f"Task with ID {task_id} not found.")
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def update_event(event_id, title, start, end, all_day):
    assert event_id is not None, "Event ID cannot be None"
    assert title is not None, "Title cannot be None"
    assert start is not None, "Start time cannot be None"
    assert end is not None, "End time cannot be None"
    assert all_day is not None, "All day cannot be None"
    print(f"Updating event with ID {event_id}...")
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Retrieve the event to be updated
            event_to_update = session.query(
                database.AppEvent).filter_by(id=event_id).first()

            if event_to_update:
                # Update the event
                event_to_update.title = title
                event_to_update.start_time = start
                event_to_update.end_time = end
                event_to_update.all_day = all_day
                session.commit()
                print(f"Event with ID {event_id} updated successfully.")
            else:
                print(f"Event with ID {event_id} not found.")
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------


def update_user_settings(user_id, earliest_time, latest_time, ideal_chunk_size, event_padding):
    assert user_id is not None, "User ID cannot be None"
    assert earliest_time is not None, "Earliest time cannot be None"
    assert latest_time is not None, "Latest time cannot be None"
    assert ideal_chunk_size is not None, "Ideal chunk size cannot be None"
    assert event_padding is not None, "Event padding cannot be None"
    print(f"Updating user settings for user with ID {user_id}...")
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Retrieve the user settings to be updated
            user_settings_to_update = session.query(
                database.AppUser).filter_by(id=user_id).first()

            if user_settings_to_update:
                # Update the user settings
                user_settings_to_update.earliest_time = earliest_time
                user_settings_to_update.latest_time = latest_time
                user_settings_to_update.ideal_chunk_size = ideal_chunk_size
                user_settings_to_update.event_padding = event_padding
                session.commit()
                print(
                    f"User settings for user with ID {user_id} updated successfully.")
            else:
                print(f"User settings for user with ID {user_id} not found.")
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
