# IT Link AI Bot - Deployment Guide

## Overview
This guide explains how to deploy the IT Link AI Bot to Render.com without manual login using GitHub Actions.

## Prerequisites
- GitHub account with access to the repository
- Render.com account
- OpenAI API key
- Facebook Page Access Token

## Deployment Steps

### Step 1: Prepare Render Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository (technologyitlink-ship-it/it-link-ai-bot)
4. Configure the service:
   - **Name**: it-link-ai-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python it_link_bot.py`
   - **Plan**: Free (or paid if needed)

### Step 2: Get Render API Key and Service ID
1. Go to Render Account Settings
2. Create an API key under "API Keys"
3. Copy the API key
4. Go to your service page and copy the Service ID from the URL (format: srv_xxxxx)

### Step 3: Configure GitHub Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `RENDER_API_KEY`: Your Render API key
   - `RENDER_SERVICE_ID`: Your Render Service ID
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PAGE_ACCESS_TOKEN`: Your Facebook Page Access Token

### Step 4: Set Environment Variables in Render
1. Go to your Render service dashboard
2. Go to "Environment" tab
3. Add the following environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PAGE_ACCESS_TOKEN`: Your Facebook Page Access Token
   - `VERIFY_TOKEN`: itlink_verify_token_123

### Step 5: Deploy
Push changes to the main branch to trigger automatic deployment:
```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

## Files Included

### render.yaml
Configuration file for Render deployment with service specifications and environment variables.

### Procfile
Specifies the command to run the web service on Render.

### .env.example
Template for environment variables (copy to .env for local development).

### deploy-to-render.yml
GitHub Actions workflow for automated deployment.

## Monitoring Deployment

1. Go to your Render service dashboard
2. Check the "Logs" tab for deployment status
3. Once deployed, your bot will be available at the provided URL

## Testing the Bot

### Webhook Verification
```bash
curl "https://your-render-url.onrender.com/?hub.mode=subscribe&hub.verify_token=itlink_verify_token_123&hub.challenge=test_challenge"
```

### Send Test Message
The bot will automatically respond to messages sent to your Facebook page.

## Troubleshooting

### Deployment Fails
- Check GitHub Actions logs for errors
- Verify all environment variables are set correctly
- Ensure the Render API key is valid

### Bot Not Responding
- Check Render service logs for errors
- Verify Facebook webhook is configured correctly
- Ensure OpenAI API key is valid
- Check Facebook Page Access Token permissions

### Environment Variables Not Loading
- Verify all variables are set in Render dashboard
- Restart the service after adding/updating variables
- Check that variable names match exactly

## Support
For issues or questions, contact: technologyitlink@gmail.com

## Additional Resources
- [Render Documentation](https://render.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Facebook Messenger Platform](https://developers.facebook.com/docs/messenger-platform)
