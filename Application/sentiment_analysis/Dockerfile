# Use an official Pytorch runtime as a parent image
FROM pytorch/pytorch:2.5.0-cuda12.4-cudnn9-runtime

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev
# Install Python dependencies for sentiment analysis
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1 

# Copy the Python scripts to the container
COPY main.py .
COPY analysis.py . 
COPY slack.py .
COPY postgres.py .

# Command to run the sentiment analysis script 
CMD ["python3", "main.py"]
