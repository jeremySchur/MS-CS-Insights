import psycopg
import os

DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),  # Service name from Docker Compose
    "port": os.getenv("POSTGRES_PORT")
}

def insert_messages(messages):
    """
        insert messages into postgres db
        :param messages: List of messages(a list of dictionaries)
        :return: None
    """
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            for message in messages:
                cur.execute("INSERT INTO message (ts, content, sentiment, user_id, channel_id) VALUES (%(ts)s, %(text)s, %(sentiment)s, %(user_id)s, %(channel_id)s) ON CONFLICT (ts) DO UPDATE SET (content, sentiment, user_id, channel_id) = (EXCLUDED.content, EXCLUDED.sentiment, EXCLUDED.user_id, EXCLUDED.channel_id);", message)
        conn.commit()

def update_timestamps(channels):
    """
        update last_read_timestamps for channels
        :param messages: List of messages(a list of dictionaries)
        :return: None
    """
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            for channel_id, channel in channels.items():
                if channel.get("last_read_timestamp"):
                    cur.execute("UPDATE channel SET last_read=%s WHERE id=%s;", (channel.get("last_read_timestamp"), channel_id))
        conn.commit()

def get_channels():
    """
        obtain a dictionary representing channels in the database
        :param None
        :return: channels object
    """
    channels = {}
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, last_read FROM channel;")
            for entry in cur:
                channels[entry[0]] = {"name": entry[1], "last_read_timestamp": entry[2]}
    return channels

def insert_channel(channel_id, channel_name):
    """
        insert channel into postgres db
        :param channel: channel dictionary
        :return: None
    """
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO channel (id, name) VALUES (%s, %s);", (channel_id, channel_name))
        conn.commit()

def update_avg_sentiments():
    """
        update average sentiments based on messages from the past day stored in the database
        :params: None
        :return: None
    """
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT channel_id, AVG(sentiment), COUNT(sentiment), COUNT(CASE WHEN sentiment > 0.3 THEN 1 END), COUNT(CASE WHEN sentiment < -0.3 THEN 1 END)
                FROM message GROUP BY channel_id;""")
            for record in cur.fetchall():
                cur.execute("UPDATE channel SET avg_sentiment = %s, num_messages = %s, num_positive = %s, num_negative = %s WHERE id = %s;", (record[1], record[2], record[3], record[4], record[0]))
            conn.commit()
