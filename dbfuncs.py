#!/usr/bin/env python

# -----------------------------------------------------------------------
# dbfuncs.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# -----------------------------------------------------------------------

# import os
import sys
import sqlalchemy
import sqlalchemy.orm
# import dotenv
import database

# dotenv.load_dotenv()
# DATABASE_URL = os.getenv['DATABASE_URL']
DATABASE_URL = 'postgresql://timemanager_c52x_user:XYwubY5k8RCdkL19NysChiHfsVgeMSCh@dpg-co0rh6a0si5c73fjt8cg-a.ohio-postgres.render.com/timemanager_c52x'

# -----------------------------------------------------------------------


def addEvent(title, start_time, end_time, all_day):
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            app_event = database.AppEvent(
                title=title,
                start_time=start_time,
                end_time=end_time,
                all_day=all_day
            )
            session.add(app_event)
            session.commit()
            return app_event.id

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# -----------------------------------------------------------------------


def getEvents():
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        with sqlalchemy.orm.Session(engine) as session:
            # Query all AppEvent objects from the database
            app_events = session.query(database.AppEvent).all()

            # Convert each AppEvent object into a dictionary
            event_dicts = []
            for event in app_events:
                event_dict = {
                    'title': event.title,
                    'start': event.start_time.isoformat(),  # Convert datetime to ISO format
                    'end': event.end_time.isoformat(),  # Convert datetime to ISO format
                    'allDay': event.all_day,
                    'id': event.id
                }
                event_dicts.append(event_dict)

        return event_dicts

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# -----------------------------------------------------------------------


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
