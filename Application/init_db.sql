-- Connect to the postgres database
\c postgres

-- Create table of Channels
CREATE TABLE IF NOT EXISTS channel (
    id VARCHAR(13) PRIMARY KEY, -- Channel_id with max length of 13 characters
    avg_sentiment DECIMAL(3, 2), -- Average sentiment score between -1.00 and 1.00
    last_read TIMESTAMP(6), -- Timestamp of last read message
    name VARCHAR(80) --slack channels can only be 80 characters long
);

-- Create table of Messages
CREATE TABLE IF NOT EXISTS message (
    ts TIMESTAMP(6) PRIMARY KEY, -- probably unique
    text TEXT,
    sentiment DECIMAL(3, 2), -- Sentiment score between -1.00 and 1.00
    user_id VARCHAR(13),
    channel_id VARCHAR(13) REFERENCES channel(id)
);





-- Previous db

/*

-- Create the sentiment_analysis table
CREATE TABLE IF NOT EXISTS sentiment_analysis (
    id SERIAL PRIMARY KEY,
    course TEXT NOT NULL,
    sentiment_score REAL NOT NULL
);

*/
