#!/usr/bin/env python

# ----------------------------------------------------------------------
# tasksplitter.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# ----------------------------------------------------------------------

import dbfuncs as database
from dateutil import parser
import datetime

class time_slot:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.num_events = 0
        self.max_num_events = int((end - start).total_seconds() / 1800)


def split_tasks(user_id, title, start, end, length, task_id):
    events = database.getEvents(user_id, [start, end])
    events.insert(0, {'start': start, 'end': start})
    events.append({'start': end, 'end': end})
    
    length = int(length)
    num_new_events = length * 2 # Assuming 30 minute chunks
    availableTimeSlots = []
    
    for i in range(len(events) - 1):
        startTime = parser.parse(events[i]['end']).replace(tzinfo=None) - datetime.timedelta(hours=4)
        endTime = parser.parse(events[i + 1]['start']).replace(tzinfo=None) - datetime.timedelta(hours=4)
        if (endTime - startTime).total_seconds() >= 1800:
            availableTimeSlots.append(time_slot(startTime, endTime))
    
    
    # Loop through all events and try to assign with modulo to availableTimeSlots
    # If availableTimeSlot[i] is full, move to next availableTimeSlot
    for i in range(num_new_events):
        j = i % len(availableTimeSlots)
        hasnt_been_assigned = True
        while hasnt_been_assigned:
            if availableTimeSlots[j].num_events < availableTimeSlots[j].max_num_events:
                availableTimeSlots[j].num_events += 1
                hasnt_been_assigned = False
            else:
                j += 1
                j = j % len(availableTimeSlots)
    
    for i in range(len(availableTimeSlots)):
        print(availableTimeSlots[i].num_events)
    
    for i in range(len(availableTimeSlots)):
        chosenSlot = availableTimeSlots[i]
        for j in range(chosenSlot.num_events):
            startTime = chosenSlot.start + datetime.timedelta(minutes=30 * j)
            endTime = startTime + datetime.timedelta(minutes=30)
            database.addEvent(user_id, title, startTime, endTime, False, task_id, "#4CAF50", None)
            