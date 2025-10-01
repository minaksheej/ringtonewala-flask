#!/usr/bin/env python3
"""
Debug script to check PORT environment variable
"""
import os
import sys

def main():
    print("=== PORT Debug Information ===")
    print(f"Python version: {sys.version}")
    print(f"Environment variables containing 'PORT':")
    
    port_vars = {k: v for k, v in os.environ.items() if 'PORT' in k.upper()}
    if port_vars:
        for key, value in port_vars.items():
            print(f"  {key} = '{value}'")
    else:
        print("  No PORT-related environment variables found")
    
    port = os.environ.get('PORT')
    print(f"\nPORT environment variable: '{port}'")
    print(f"Type: {type(port)}")
    
    if port:
        try:
            port_int = int(port)
            print(f"As integer: {port_int}")
            print(f"Valid port: {1 <= port_int <= 65535}")
        except ValueError:
            print(f"Invalid port format: '{port}'")
    
    print("\n=== Test gunicorn command ===")
    test_port = port or '8000'
    cmd = f"gunicorn --bind 0.0.0.0:{test_port} --workers 1 --timeout 30 app:app"
    print(f"Command: {cmd}")
    
    print("\n=== All environment variables ===")
    for key, value in sorted(os.environ.items()):
        if 'PORT' in key.upper() or 'RAILWAY' in key.upper():
            print(f"{key} = {value}")

if __name__ == '__main__':
    main()
