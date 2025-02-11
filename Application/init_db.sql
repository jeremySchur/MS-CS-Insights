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
    content TEXT,
    sentiment DECIMAL(3, 2), -- Sentiment score between -1.00 and 1.00
    user_id VARCHAR(13),
    channel_id VARCHAR(13) REFERENCES channel(id)
);



-- NOTE: For this db to start existing in the db-volume folder
-- I had to remove the db with
-- rm -rf ./db/*
-- Then restart docker

-- Create table for Users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,        -- Auto-incrementing unique identifier
    username VARCHAR(50) UNIQUE NOT NULL, -- Username with a maximum length of 50 characters
    password VARCHAR(255) NOT NULL -- Password
);

-- -- Insert sample users for testing
-- INSERT INTO users (username, password)
-- VALUES 
--     ('jeremy', 'password123'),
--     ('sang', 'securepass'),
--     ('owen', 'admin123');
