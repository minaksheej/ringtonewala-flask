# Railway Deployment Guide

This guide explains how to deploy the RingtoneWala Flask application to Railway with FFmpeg support.

## Quick Deployment

### Method 1: Docker Deployment (Recommended)

1. **Push to GitHub**: Make sure your code is pushed to a GitHub repository
2. **Connect to Railway**:
   - Go to [Railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
3. **Railway will automatically detect the Dockerfile and deploy**

### Method 2: Nixpacks Deployment

If you prefer Nixpacks over Docker:

1. **Use the nixpacks.toml configuration** (already included)
2. **Railway will automatically install FFmpeg** using the Nix package manager

## Environment Variables

Set these in your Railway project settings:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
PORT=8000
```

## FFmpeg Installation

### Docker Method (Automatic)

- FFmpeg is automatically installed via the Dockerfile
- No additional configuration needed

### Nixpacks Method (Automatic)

- FFmpeg is automatically installed via nixpacks.toml
- No additional configuration needed

## Troubleshooting

### FFmpeg Not Found Error

If you see "ffprobe and ffmpeg not found":

1. **Check deployment method**: Ensure you're using Docker or Nixpacks
2. **Check logs**: Look for FFmpeg installation messages in Railway logs
3. **Verify environment**: The app checks for FFmpeg on startup

### Build Failures

1. **Check Dockerfile**: Ensure it includes FFmpeg installation
2. **Check nixpacks.toml**: Ensure it includes FFmpeg package
3. **Check logs**: Look for specific error messages

## Local Testing

Before deploying, test locally:

```bash
# Build and run Docker container
docker build -t ringtonewala .
docker run -p 8000:8000 ringtonewala
```

## Performance Tips

1. **Use appropriate worker count**: The app uses 2 Gunicorn workers by default
2. **Set timeout**: 120 seconds timeout for long audio processing
3. **Monitor resources**: Railway provides resource usage metrics

## Custom Domain

1. Go to Railway project settings
2. Add your custom domain
3. Update the DOMAIN environment variable
4. Configure DNS records as instructed by Railway
