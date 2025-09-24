# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app

# Make startup script executable and ensure proper ownership
RUN chmod +x start.sh && chown app:app start.sh
RUN chmod +x run_app.py && chown app:app run_app.py
USER app

# Expose port (Railway typically uses 8000, but we'll use the env var in CMD)
EXPOSE 8000

# Run the application using Python script that handles PORT properly
CMD ["python", "run_app.py"]
