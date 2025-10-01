#!/bin/bash

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting Flask app on port $PORT"

# Start the application using Python script for better PORT handling
exec python run_app.py
