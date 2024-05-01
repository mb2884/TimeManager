SELECT * FROM app_event;
SELECT * FROM app_task;
SELECT * FROM app_user;

DROP TABLE IF EXISTS app_event;
DROP TABLE IF EXISTS app_task;
DROP TABLE IF EXISTS app_user CASCADE;

      
CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    earliest_time TIME(0) DEFAULT '08:00:00' NOT NULL,
    latest_time TIME(0) DEFAULT '20:00:00' NOT NULL,
    ideal_chunk_size INT DEFAULT 60 NOT NULL,
    event_padding INT DEFAULT 10 NOT NULL
);


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

CREATE TABLE app_event (
    id SERIAL PRIMARY KEY,
    user_id INT,
    group_id INT,
    title TEXT,
    descrip TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    all_day BOOLEAN,
    parent_task_id INT,
    color TEXT,
    days_of_week TEXT,
    start_recur TIMESTAMP,
    end_recur TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES app_user(id),
    FOREIGN KEY (parent_task_id) REFERENCES app_task(id) ON DELETE CASCADE
);



