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

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# ----------------------------------------------------------------------

def get_user_id(username):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Query the AppUser object from the database
            app_user = session.query(database.AppUser).filter_by(username=username).first()

            if app_user:
                return app_user.id
            else:
                # Create a new AppUser entry for the username
                new_user = database.AppUser(username=username)
                session.add(new_user)
                session.commit()
                return new_user.id

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------

def addEvent(user_id, title, start_time, end_time, all_day, parent_task_id=None, color=None):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            app_event = database.AppEvent(
                user_id=user_id,
                title=title,
                start_time=start_time,
                end_time=end_time,
                all_day=all_day,
                parent_task_id=parent_task_id,
                color=color
            )
            session.add(app_event)
            session.commit()
            return app_event.id

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------

def addTask(user_id, title, start_time, due_date, est_length):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            app_task = database.AppTask(
                user_id=user_id,
                title=title,
                start_time=start_time,
                due_date=due_date,
                est_length = est_length
            )
            session.add(app_task)
            session.commit()
            return app_task.id

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------

def getEvents(user_id, filter_by_date=None):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:

            if filter_by_date:
                app_events = session.query(database.AppEvent).filter_by(user_id=user_id).filter(database.AppEvent.start_time >= filter_by_date[0]).filter(database.AppEvent.end_time <= filter_by_date[1]).order_by(database.AppEvent.start_time).all()
            else:
                app_events = session.query(database.AppEvent).filter_by(user_id=user_id).all()

            # Convert each AppEvent object into a dictionary
            event_dicts = []
            for event in app_events:
                event_dict = {
                    'title': event.title,
                    'start': event.start_time.isoformat(),  # Convert datetime to ISO format
                    'end': event.end_time.isoformat(),  # Convert datetime to ISO format
                    'allDay': event.all_day,
                    'id': event.id,
                    'parentTaskID': event.parent_task_id,
                    'color': event.color
                }
                event_dicts.append(event_dict)

        return event_dicts

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# -----------------------------------------------------------------------

def getTasks(user_id):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Query all AppEvent objects from the database
            app_tasks = session.query(database.AppTask).filter_by(user_id=user_id).all()

            # Convert each AppEvent object into a dictionary
            task_dicts = []
            for task in app_tasks:
                task_dict = {
                    'title': task.title,
                    'start': task.start_time.isoformat() if task.start_time else None,  # Convert datetime to ISO format
                    'end': task.due_date.isoformat() if task.due_date else None,  # Convert datetime to ISO format
                    'length': task.est_length,
                    'id': task.id
                }
                task_dicts.append(task_dict)
        return task_dicts

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)


#-----------------------------------------------------------------------


def delete_event(event_id):
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

def update_event(event_id, title, start, end, all_day):
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