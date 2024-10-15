-- Connect to the postgres database
\c postgres

-- Create the sentiment_analysis table
CREATE TABLE IF NOT EXISTS sentiment_analysis (
    id SERIAL PRIMARY KEY,
    course TEXT NOT NULL,
    sentiment_score REAL NOT NULL
);