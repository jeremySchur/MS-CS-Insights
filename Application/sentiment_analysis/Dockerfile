FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src src

FROM base AS final
ENV PYTHONUNBUFFERED=1 
CMD ["python3", "src/main.py"]
