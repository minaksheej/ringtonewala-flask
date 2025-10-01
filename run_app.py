#!/usr/bin/env python3
"""
Railway deployment script that handles PORT environment variable properly
"""
import os
import subprocess
import sys

def main():
    # Get PORT from environment, default to 8000
    port = os.environ.get('PORT', '8000')
    
    # Validate port number
    try:
        port_int = int(port)
        if port_int < 1 or port_int > 65535:
            raise ValueError("Port out of range")
    except (ValueError, TypeError):
        print(f"Invalid PORT value: '{port}', using default 8000")
        port = '8000'
    
    print(f"Starting Flask app on port {port}")
    print(f"Environment variables: PORT={os.environ.get('PORT', 'NOT_SET')}")
    
    # Build gunicorn command
    cmd = [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
        'app:app'
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Run gunicorn
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running gunicorn: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)

if __name__ == '__main__':
    main()
