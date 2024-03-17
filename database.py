#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# Based on content from ChatGPT
#-----------------------------------------------------------------------

import sqlite3
import contextlib
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

#-----------------------------------------------------------------------

_DATABASE_URL = 'file:penny.sqlite?mode=ro'

#-----------------------------------------------------------------------

Base = declarative_base()

# User table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)


# Table for user events
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0 for Monday, 1 for Tuesday, ..., 6 for Sunday


# Table for user tasks
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    task_name = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    estimated_hours = Column(Integer, nullable=False)
    completed = Column(Boolean, default=False)

# Initialize database connection
engine = create_engine('sqlite:///timemanager.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)