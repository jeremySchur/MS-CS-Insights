-- Connect to the postgres database
\c postgres

-- Create table of Channels
CREATE TABLE IF NOT EXISTS channel_sentiments (
    channel_id VARCHAR(13) PRIMARY KEY, -- Channel_id with max length of 13 characters
    avg_sentiment DECIMAL(3, 2) -- Average sentiment score between -1.00 and 1.00
);

-- Create table of Messages for each Channel
CREATE TABLE IF NOT EXISTS messages_sentiments (
    message_ts TIMESTAMP(3) PRIMARY KEY, -- Timestamp with milliseconds percision
    message_text TEXT,
    sentiment_score DECIMAL(3, 2), -- Sentiment score between -1.00 and 1.00
    processed BOOLEAN, -- Indicates if this message has been analyzed
    channel_id TEXT,
    FOREIGN KEY (channel_id) REFERENCES channel_sentiments(channel_id)
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