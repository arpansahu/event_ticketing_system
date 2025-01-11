# Base image
FROM python:3.12-slim

# Install PostgreSQL client and dependencies
RUN apt-get update && apt-get install -y \
    build-essential gcc libc-dev libpq-dev libev-dev sqlite3 postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app
ENV PYTHONPATH="/app"

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app/

# Expose Django port
EXPOSE 8000

# Default command to run migrations, seed database, and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed && python manage.py runserver 0.0.0.0:8000"]
