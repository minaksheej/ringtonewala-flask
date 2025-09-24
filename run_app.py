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
    
    print(f"Starting Flask app on port {port}")
    
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
