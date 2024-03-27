#!/usr/bin/env python

#-----------------------------------------------------------------------
# dbfuncs.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
#-----------------------------------------------------------------------

# import os
import sys
import sqlalchemy
import sqlalchemy.orm
# import dotenv
import database

# dotenv.load_dotenv()
# DATABASE_URL = os.getenv['DATABASE_URL']
DATABASE_URL = 'postgresql://timemanager_c52x_user:XYwubY5k8RCdkL19NysChiHfsVgeMSCh@dpg-co0rh6a0si5c73fjt8cg-a.ohio-postgres.render.com/timemanager_c52x'

#-----------------------------------------------------------------------

def addEvent(title, start_time, end_time, all_day):
    
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        database.Base.metadata.drop_all(engine)
        database.Base.metadata.create_all(engine)

        with sqlalchemy.orm.Session(engine) as session:

            #-----------------------------------------------------------
            app_event = database.app_event(title = title,
                                   start_time = start_time,
                                   end_time = end_time,
                                   all_day = all_day)
            session.add(app_event)
            session.commit()

        engine.dispose()

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

def getEvents():
    
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)

        database.Base.metadata.drop_all(engine)
        database.Base.metadata.create_all(engine)

        with sqlalchemy.orm.Session(engine) as session:

            #-----------------------------------------------------------
            app_event = session.query(database.app_event).all()

            engine.dispose()

            return app_event

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------
