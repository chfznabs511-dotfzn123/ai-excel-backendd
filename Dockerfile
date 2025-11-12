# Dockerfile for AI Excel App (Render-ready)

# 1. Use an official Python runtime
FROM python:3.11.9-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory
WORKDIR /app

# 4. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy app code
COPY . .

# 6. Use shell form CMD so $PORT is expanded at runtime
CMD gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app
