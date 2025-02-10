# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /server

# Install FastAPI and other dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to disable output buffering
ENV PYTHONUNBUFFERED=1

# Copy the FastAPI app code into the container
COPY /app .

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]