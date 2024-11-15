from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from pydantic import BaseModel
from typing import List
import os

# Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")  # Default to localhost:3000)
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

# Pydantic model for user login
class LoginRequest(BaseModel):
    username: str
    password: str



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
    cursor.execute("SELECT name, avg_sentiment FROM channel")
    data = cursor.fetchall()

    # Close connection
    cursor.close()
    conn.close()

    # Return the fetched data as a list of SentimentAnalysis objects
    return [SentimentAnalysis(name=row[0], avg_sentiment=row[1]) for row in data]

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

@app.post("/api/login")
async def login(request: LoginRequest):
    # Connect to the database
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    
    # Execute a query to find the user with the provided username and password
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (request.username, request.password))
    user = cursor.fetchone()

    # Close the database connection
    cursor.close()
    conn.close()

    # Check if a matching user was found
    if user:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
