# Deployment Guide for Telegram Bot

## Overview

This guide covers the deployment fixes applied to resolve Cloud Run autoscale deployment issues and prevent multiple bot instance conflicts.

## Applied Fixes

### ✅ 1. Port Binding for Cloud Run
- Added proper port configuration with `PORT` environment variable
- Server binds to `0.0.0.0:PORT` for external accessibility
- Default ports: 8080 (production), 5000 (development)

### ✅ 2. Webhook Support for Production
- Implemented webhook mode for production deployments
- Added health check endpoints (`/health`, `/`)
- Automatic webhook URL configuration for Cloud Run environments
- Graceful fallback when webhook URL is not available

### ✅ 3. Environment Detection
- Automatic environment detection (development vs production)
- Cloud Run detection via `K_SERVICE` and `GOOGLE_CLOUD_PROJECT` variables
- Production mode uses webhooks, development uses polling

### ✅ 4. Single Instance Management
- Process monitoring to detect existing bot instances
- Automatic termination of conflicting processes
- Graceful shutdown handlers for clean exits

### ✅ 5. Health Check Endpoints
- `/health` endpoint for autoscale health checks
- `/` root endpoint returns 200 OK status
- Proper HTTP response handling for deployment monitoring

## Deployment Configuration

### Environment Variables

**Required:**
- `TELEGRAM_TOKEN` - Bot token from @BotFather
- `OPENAI_API_KEY` - OpenAI API key
- `ASSISTANT_ID` - OpenAI Assistant ID

**Deployment-specific:**
- `ENVIRONMENT` - `development` or `production` (auto-detected)
- `PORT` - Server port (auto-set: 8080 for production, 5000 for dev)
- `WEBHOOK_URL` - Webhook URL for production (auto-generated for Cloud Run)

### Deployment Scripts

**Development (Replit):**
```bash
ALLOWED_USERS=7668792787 python start.py
```

**Production (Cloud Run):**
```bash
ENVIRONMENT=production PORT=8080 ALLOWED_USERS=7668792787 python start.py
```

**Manual deployment:**
```bash
chmod +x deploy.sh
./deploy.sh
```

## Architecture Changes

### New Files
- `start.py` - Enhanced startup script with deployment fixes
- `deploy.sh` - Production deployment script
- `DEPLOYMENT.md` - This deployment guide

### Modified Files
- `main.py` - Added webhook support and health endpoints
- `config.py` - Added deployment configuration options

### Dependencies Added
- `aiohttp` - Web server for webhook endpoints
- `psutil` - Process management for instance control

## Production Deployment Process

### 1. Cloud Run Deployment
1. Set `ENVIRONMENT=production`
2. Configure required environment variables
3. Deploy using provided deployment script
4. Webhook URL will be auto-configured

### 2. Manual Webhook Configuration
If auto-configuration fails:
```bash
# Set webhook manually after deployment
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://your-app-url.com/webhook"
```

### 3. Health Check Verification
```bash
curl https://your-app-url.com/health
# Should return: OK
```

## Troubleshooting

### Multiple Instance Conflicts
- The startup script automatically kills existing instances
- Check logs for "Stopped X existing bot instances" message

### Webhook Setup Issues
- Verify `WEBHOOK_URL` environment variable
- Check Telegram webhook status: `/getWebhookInfo`
- Ensure HTTPS is used for webhook URL

### Port Binding Issues
- Verify `PORT` environment variable is set
- Check firewall settings for the specified port
- Ensure application binds to `0.0.0.0` not `localhost`

## Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| Mode | Polling | Webhooks |
| Port | Not required | Required (8080) |
| Health Check | Not available | Available |
| Instance Management | Basic | Advanced |
| Environment Detection | Manual | Automatic |

## Status

All suggested deployment fixes have been successfully implemented:
- ✅ Port binding for Cloud Run autoscale
- ✅ Webhook support for production
- ✅ Environment variable configuration
- ✅ Single instance management
- ✅ Health check endpoints

The bot is now ready for production deployment on Cloud Run or similar container platforms.