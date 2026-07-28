# Use official Python image
FROM python:3.12-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Flush logs immediately
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install project
RUN pip install -e .

# Install additional dependencies if required
RUN pip install flask python-dotenv

# Expose Flask port
EXPOSE 8080

# Start Flask app
CMD ["python", "app.py"]