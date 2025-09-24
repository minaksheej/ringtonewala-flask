# Deployment Guide - Railway

This guide will help you deploy your RingtoneWala.com application to Railway.

## Prerequisites

1. A GitHub account
2. A Railway account (sign up at [railway.app](https://railway.app))
3. Your code pushed to a GitHub repository

## Step 1: Prepare Your Repository

Make sure your repository contains all the necessary files:

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `railway.json` - Railway configuration
- `Procfile` - Process file for Railway
- `runtime.txt` - Python version specification

## Step 2: Deploy to Railway

1. **Connect to Railway:**

   - Go to [railway.app](https://railway.app) and sign in
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Configure Environment Variables:**

   - In Railway dashboard, go to your project
   - Click on "Variables" tab
   - Add the following environment variables:
     ```
     SECRET_KEY=your-random-secret-key-here
     DEBUG=False
     PORT=8000
     ```

3. **Deploy:**
   - Railway will automatically detect your Python app
   - It will install dependencies from `requirements.txt`
   - The app will be deployed and you'll get a public URL

## Step 3: Custom Domain (Optional)

1. In Railway dashboard, go to "Settings"
2. Click "Domains"
3. Add your custom domain
4. Update your DNS settings as instructed

## Step 4: SEO Optimization

After deployment, update these URLs in your code:

- Update all `https://audioconverter-pro.railway.app` references to your actual domain
- Update the sitemap.xml route with your domain
- Update robots.txt with your domain

## Step 5: Monitor and Maintain

1. **Monitor Logs:**

   - Use Railway's built-in logging
   - Check for any errors or performance issues

2. **Update Dependencies:**

   - Regularly update packages in `requirements.txt`
   - Redeploy when needed

3. **Backup:**
   - Your code is backed up in GitHub
   - Consider database backups if you add persistent storage

## Environment Variables Reference

| Variable     | Description                   | Default  |
| ------------ | ----------------------------- | -------- |
| `SECRET_KEY` | Flask secret key for sessions | Required |
| `DEBUG`      | Enable debug mode             | `False`  |
| `PORT`       | Port for the application      | `8000`   |

## Troubleshooting

### Common Issues:

1. **Build Fails:**

   - Check `requirements.txt` for syntax errors
   - Ensure all dependencies are compatible

2. **App Won't Start:**

   - Check Railway logs for error messages
   - Verify environment variables are set

3. **Performance Issues:**
   - Monitor Railway's metrics
   - Consider upgrading your Railway plan

### Support:

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)

## Security Considerations

1. **Secret Key:**

   - Use a strong, random secret key
   - Never commit secrets to your repository

2. **HTTPS:**

   - Railway provides HTTPS by default
   - Ensure your custom domain also uses HTTPS

3. **File Uploads:**
   - Current implementation uses temporary files
   - Consider implementing file size limits for production

## Scaling

Railway offers different plans:

- **Hobby Plan:** Free tier with limitations
- **Pro Plan:** Higher limits and better performance
- **Team Plan:** For team collaboration

Choose the plan that fits your needs and budget.
