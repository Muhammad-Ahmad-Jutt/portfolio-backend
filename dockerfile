FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies needed for some packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libcairo2-dev \
    libgirepository1.0-dev \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxrandr-dev \
    python3-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install Python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose default port for your app if needed
EXPOSE 5000
