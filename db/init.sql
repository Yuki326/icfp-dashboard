-- init.sql

CREATE DATABASE IF NOT EXISTS mydatabase;

USE mydatabase;

CREATE TABLE IF NOT EXISTS problems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    problem_id INT,
    user_input TEXT,
    request_text TEXT,
    result TEXT,
    submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

CREATE TABLE IF NOT EXISTS answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    problem_id INT,
    answer_text TEXT,
    answer_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

INSERT INTO problems (title) VALUES ('Sample Problem 1');
-- INSERT INTO submissions (problem_id, user_input ,request_text, result) VALUES (1, 'Sample Submission 1','sample' 'Sample Response 1');