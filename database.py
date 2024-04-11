#!/usr/bin/env python

# -----------------------------------------------------------------------
# database.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# -----------------------------------------------------------------------

import sqlalchemy.ext.declarative
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()


class AppUser(Base):
    __tablename__ = 'app_user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.Text)


class AppEvent(Base):
    __tablename__ = 'app_event'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('app_user.id'))
    group_id = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.Text)
    descrip = sqlalchemy.Column(sqlalchemy.Text)
    start_time = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    end_time = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    all_day = sqlalchemy.Column(sqlalchemy.Boolean)


class AppTask(Base):
    __tablename__ = 'app_task'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('app_user.id'))
    group_id = sqlalchemy.Column(sqlalchemy.Integer)
    title = sqlalchemy.Column(sqlalchemy.Text)
    descrip = sqlalchemy.Column(sqlalchemy.Text)
    start_time = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    due_date = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    est_length = sqlalchemy.Column(sqlalchemy.REAL)



