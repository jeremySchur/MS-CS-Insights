CREATE TABLE sentiments (
    id SERIAL PRIMARY KEY,
    course_name VARCHAR(300),
    sentiment_score DECIMAL(3, 2) CHECK (sentiment_score >= 0 AND sentiment_score <= 1)
);


CREATE TABLE word_counts (
    word VARCHAR(46) PRIMARY KEY,
    count INT
);


/*
-- Example actions with table: sentiments --

INSERT INTO sentiments (course_name, sentiment_score) VALUES
('Data Science', 0.01),
('Cyber Security', 0.67);

SELECT * FROM sentiments;

UPDATE sentiments
SET sentiment_score = 0.94
WHERE course_name = 'Cyber Security';





-- Example actions with table: word_counts --

INSERT INTO word_counts (word, count) VALUES
('hat', 4),
('fun', 34),
('collected', 10);

SELECT * FROM word_counts;

UPDATE word_counts
SET count = count + 1
WHERE word = 'hat';
*/
