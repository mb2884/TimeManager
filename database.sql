DROP TABLE IF EXISTS app_user;
DROP TABLE IF EXISTS app_event;
DROP TABLE IF EXISTS app_task;


CREATE TABLE app_user (
    id INT PRIMARY KEY,
    username TEXT
);
-- Defines a table for events, which describe prior time conflicts
CREATE TABLE app_event (
    id INT PRIMARY KEY,
    user_id INT,
    group_id INT,
    title TEXT,
    descrip TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    all_day BOOLEAN
);
-- Defines a table for tasks, which are time-bound activities
CREATE TABLE app_task (
    id INT PRIMARY KEY,
    user_id INT,
    event_id INT,
    group_id INT,
    title TEXT,
    descrip TEXT,
    start_time TIMESTAMP,
    due_date TIMESTAMP,
    est_length REAL
);

