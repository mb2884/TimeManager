#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
#-----------------------------------------------------------------------

import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()

class app_user(Base):
    __tablename__ = 'app_user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.Text)

class app_event(Base):
    __tablename__ = 'app_event'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    group_id = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.Text)
    descrip = sqlalchemy.Column(sqlalchemy.Text)
    start_time = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    end_time = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    all_day = sqlalchemy.Column(sqlalchemy.Boolean)

class app_task(Base):
    __tablename__ = 'app_task'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    event_id = sqlalchemy.Column(sqlalchemy.Integer)
    group_id = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.Text)
    descrip = sqlalchemy.Column(sqlalchemy.Text)
    start_time = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    due_date = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    est_length = sqlalchemy.Column(sqlalchemy.REAL)