# Dockerfile for Flask app deployment on Render

# 1. Use official Python 3.11.9 slim image
FROM python:3.11.9-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000

# 3. Set working directory
WORKDIR /app

# 4. Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libssl-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copy app code
COPY . .

# 7. Run the app with Gunicorn
# Using shell form to allow $PORT expansion
CMD gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app
