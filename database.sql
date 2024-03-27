SELECT * FROM app_event;

DROP TABLE IF EXISTS app_event;
DROP TABLE IF EXISTS app_task;
DROP TABLE IF EXISTS app_user CASCADE;


CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    username TEXT
);
-- Defines a table for events, which describe prior time conflicts
CREATE TABLE app_event (
    id SERIAL PRIMARY KEY,
    user_id INT,
    group_id INT,
    title TEXT,
    descrip TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    all_day BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES app_user(id)
);
-- Defines a table for tasks, which are time-bound activities
CREATE TABLE app_task (
    id SERIAL PRIMARY KEY,
    user_id INT,
    group_id INT,
    title TEXT,
    descrip TEXT,
    start_time TIMESTAMP,
    due_date TIMESTAMP,
    est_length REAL,
    FOREIGN KEY (user_id) REFERENCES app_user(id)
);

