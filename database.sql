CREATE TABLE user (
    id INT PRIMARY KEY,
    username TEXT
);
-- Defines a table for events, which describe prior time conflicts
CREATE TABLE event (
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
CREATE TABLE task (
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

