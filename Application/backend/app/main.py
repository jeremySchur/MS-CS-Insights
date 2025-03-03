from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel
from datetime import datetime
from typing import List
import os

# Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL")
# PostgreSQL connection parameters
DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),  # Service name from Docker Compose
    "port": os.getenv("POSTGRES_PORT")
}

# Pydantic model for sentiment analysis data
class SentimentAnalysis(BaseModel):
    name: str
    avg_sentiment: float | None
    num_messages: int | None
    num_positive: int | None
    num_negative: int | None
    last_read: str | None


# FastAPI app instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=List[SentimentAnalysis])
async def root():
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    # Execute query to retrieve data
    cursor.execute("SELECT name, avg_sentiment, last_read, num_messages, num_positive, num_negative FROM channel ORDER BY last_read DESC NULLS LAST")
    data = cursor.fetchall()

    # Close connection
    cursor.close()
    conn.close()

    # Return the fetched data as a list of SentimentAnalysis objects
    return [SentimentAnalysis(name=row[0], avg_sentiment=row[1], last_read=row[2],  num_messages = row[3], num_positive = row[4], num_negative = row[5]) for row in data]

# @app.post("/test", response_model=SentimentAnalysis)
# async def test(sa: SentimentAnalysis):
#     conn = psycopg2.connect(**DB_PARAMS)
#     cursor = conn.cursor()

#     # Execute query to insert data
#     cursor.execute(
#         "INSERT INTO sentiment_analysis (course, sentiment_score) VALUES (%s, %s)",
#         (sa.course, sa.sentiment_score)
#     )

#     # Commit the transaction
#     conn.commit()

#     # Close connection
#     cursor.close()
#     conn.close()

#     # Return the inserted SentimentAnalysis object
#     return sa

class CourseMessage(BaseModel):
    ts: str
    content: str
    score: float

@app.get("/course/", response_model=List[CourseMessage])
async def course(name: str):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    # raise Exception(f"name: {str(name)}, {type(name)}")
    cursor.execute("SELECT id FROM channel WHERE name = %s", (name,))
    channel_id = cursor.fetchall()[0]

    # Execute query to retrieve data
    cursor.execute("SELECT ts, content, sentiment FROM message WHERE channel_id = %s ORDER BY ts DESC", (channel_id,))
    data = cursor.fetchall()

    # Close connection
    cursor.close()
    conn.close()

    # Return the fetched data as a list of SentimentAnalysis objects
    return [CourseMessage(ts=row[0], content=row[1], score=row[2]) for row in data]
