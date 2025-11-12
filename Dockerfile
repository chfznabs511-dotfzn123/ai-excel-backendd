# 1. Use official Python runtime
FROM python:3.11.9-slim

# 2. Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set working directory
WORKDIR /app

# 4. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Expose port for Render
EXPOSE 10000

# 7. Start the Flask app using Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app
