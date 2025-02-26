from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import psycopg2
from pydantic import BaseModel
from typing import List
import os
import bcrypt


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
    email: str
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

class LoginRequest(BaseModel):
    email: str
    password: str

def hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def insert_dummy_users():
    dummy_users = {
        "jeremy@jeremy.com": "password123",
    }
    
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    for email, password in dummy_users.items():
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone() is None:
            hashed_password = hash_password(password)
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))

    conn.commit()
    cursor.close()
    conn.close()

@app.on_event("startup")
def startup_event():
    insert_dummy_users()

@app.post("/api/login")
async def login(request: LoginRequest):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE email = %s", (request.email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and verify_password(request.password, user[0]):
        return {"message": "Login successful", "user": request.email}
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

@app.get("/api/logout")
async def logout():
    return {"message": "User logged out"}

@app.get("/api/force-logout")
async def force_logout():
    return {"message": "Forced logout on login page"}