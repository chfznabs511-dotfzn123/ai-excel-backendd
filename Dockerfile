# Dockerfile # Docker configuration for deployment

# 1. Use an official Python runtime as a parent image
# Using the slim-buster version for a smaller image size. Matched to Render's supported version.
FROM python:3.11.9-slim

# 2. Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1
# Set the port the application will run on
ENV PORT 10000

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install dependencies
# Copy the requirements file first to leverage Docker's layer caching.
# This step will only be re-run if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application's code into the container
COPY . .

# 6. Command to run the application
# Use gunicorn as a production-ready WSGI server.
# It will listen on the port specified by the PORT environment variable.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "4", "app:app"]
