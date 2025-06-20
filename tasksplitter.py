#!/usr/bin/env python

# ----------------------------------------------------------------------
# tasksplitter.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
# ----------------------------------------------------------------------

import dbfuncs as database
from dateutil import parser
import datetime
import pytz

# ----------------------------------------------------------------------`

nytz = pytz.timezone('America/New_York')

# ----------------------------------------------------------------------


def split_tasks(user_id, title, start, end, length, task_id,  calendar_events):
    work_start_time, work_end_time, ideal_chunk_length, event_padding = database.get_user_settings(
        user_id)

    assert (
        all(val is not None for val in [work_start_time, work_end_time, ideal_chunk_length,
            event_padding, start, end, length, task_id, calendar_events, title, user_id])
    ), "One or more arguments are None"

    # Format work_start_time and work_end_time
    work_start_time = work_start_time.hour
    work_end_time = work_end_time.hour

    # print("User settings: ", work_start_time,
    #       work_end_time, ideal_chunk_length, event_padding)

    # Get all events from the database that overlap with the task
    events = [event for event in calendar_events if not event['allDay'] and parser.parse(event['start']).replace(
        tzinfo=nytz) < end.replace(tzinfo=nytz) and parser.parse(event['end']).replace(tzinfo=nytz) > start.replace(tzinfo=nytz)]
    event_times = {}
    current_day = start.replace(tzinfo=nytz)

    end_day = end.replace(tzinfo=nytz)


    while current_day <= end_day:
        event_times[current_day.date()] = 0
        current_day += datetime.timedelta(days=1)

    for event in events:
        event_start = parser.parse(event['start']).replace(tzinfo=nytz)
        event_end = parser.parse(event['end']).replace(tzinfo=nytz)
        current_day = event_start.date()
        while current_day < event_end.date():
            event_times[current_day] += (datetime.datetime.combine(
                current_day, datetime.time(hour=work_end_time)) - event_start).total_seconds() / 60
            event_start = datetime.datetime.combine(
                current_day, datetime.time(hour=work_start_time))
            current_day += datetime.timedelta(days=1)
        event_times[current_day] += (event_end -
                                     event_start).total_seconds() / 60

    time_left_in_task = length * 60
    k = 1

    while time_left_in_task > 0:
        print("K: ", k)
        if k > len(event_times):

            raise Exception("Not enough time to schedule task")

        if time_left_in_task <= 0:

            break

        min_day = [y[0] for y in sorted(
            event_times.items(), key=lambda x: x[1])[:k]][-1]
        # Check if the day is the first day in which case we need to start at the start time of the task
        if min_day == start.date():
            current_day = start.replace(tzinfo=nytz)
        else:
            current_day = datetime.datetime.combine(
                min_day, datetime.time(hour=work_start_time)).replace(tzinfo=nytz)
        
        # Insert the task into the day at ideal_chunk_length intervals at the earliest time slot from work_start_time to work_end_time such that the task does not overlap with any events and their padding
        # Being cognizant of the fact that work_end_time may be later than end_day

        while current_day < datetime.datetime.combine(min_day, datetime.time(hour=work_end_time)).replace(tzinfo=nytz) and time_left_in_task > 0:
            # Check if the current time slot overlaps with any events
            overlap = False
            for event in events:
                event_start = parser.parse(event['start']).replace(tzinfo=nytz)
                event_end = parser.parse(event['end']).replace(tzinfo=nytz)
                
                if current_day < event_end and current_day + datetime.timedelta(minutes=ideal_chunk_length) > event_start:
                    overlap = True
                    continue
            if not overlap:
                chunk_start = current_day
                chunk_end = current_day + \
                    datetime.timedelta(minutes=min(
                        ideal_chunk_length, time_left_in_task))
                

                # add to database
                database.addEvent(user_id, title, chunk_start.replace(tzinfo=None), chunk_end.replace(
                    tzinfo=None), False, task_id, "#4CAF50", None, None, None)
                # add to events
                events.append({'title': title, 'start': chunk_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"), 'end': chunk_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"), 'allDay': False, 'id': None,
                              'parentTaskID': task_id, 'color': "#4CAF50", 'daysOfWeek': None, 'startRecur': None, 'endRecur': None, 'startTime': chunk_start.time().isoformat(), 'endTime': chunk_end.time().isoformat()})
                time_left_in_task -= (chunk_end -
                                      chunk_start).total_seconds() / 60
                # Update the event_times dictionary
                event_times[min_day] += (chunk_end -
                                         chunk_start).total_seconds() / 60

                min_day = [y[0] for y in sorted(
                    event_times.items(), key=lambda x: x[1])[:k]][-1]
                # Check if the day is the first day in which case we need to start at the start time of the task
                if min_day == start.date():
                    current_day = start.replace(tzinfo=nytz)
                else:
                    current_day = datetime.datetime.combine(
                        min_day, datetime.time(hour=work_start_time)).replace(tzinfo=nytz)

                continue
            current_day += datetime.timedelta(
                minutes=ideal_chunk_length + event_padding)

        
        k += 1


# ----------------------------------------------------------------------
