#!/bin/bash

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting Flask app on port $PORT"

# Start the application
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
