# Use official lightweight Python image
FROM python:3.11.9-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Render's port
EXPOSE 10000

# Start Gunicorn server (Render automatically sets $PORT)
CMD echo "🚀 Starting Flask backend on Render..." && \
    gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app
