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
    earliest_time = sqlalchemy.Column(sqlalchemy.TIME)
    latest_time = sqlalchemy.Column(sqlalchemy.TIME)
    ideal_chunk_size = sqlalchemy.Column(sqlalchemy.Integer)
    event_padding = sqlalchemy.Column(sqlalchemy.Integer)


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
    parent_task_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('app_task.id'))
    color = sqlalchemy.Column(sqlalchemy.Text)
    days_of_week = sqlalchemy.Column(sqlalchemy.Text)
    start_recur = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    end_recur = sqlalchemy.Column(sqlalchemy.TIMESTAMP)


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
