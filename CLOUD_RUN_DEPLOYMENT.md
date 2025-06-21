# Cloud Run Deployment Guide

## Current Status
- Bot fully operational with conflict prevention system
- All features working: messaging, OpenAI integration, authorization, logging
- Deployment scripts ready with automatic instance management

## Deployment Options

### Option 1: Replit Deploy (Webhook Mode)
W Build command wpisz:
```bash
./deploy_script.sh
```

Następnie wybierz **Autoscale** - bot automatycznie przejdzie na webhook mode

### Option 2: Manual Cloud Run Deployment
```bash
# Build and deploy with conflict prevention
gcloud run deploy salesupply-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000 \
  --set-env-vars="TELEGRAM_TOKEN=${TELEGRAM_TOKEN},OPENAI_API_KEY=${OPENAI_API_KEY},ASSISTANT_ID=asst_qgWQNNJGV0bGPy35Rdif4qpb,ALLOWED_USERS=7668792787"
```

### Option 3: Advanced Build Pipeline
```bash
# Use Cloud Build with automated conflict resolution
gcloud builds submit --config cloudbuild.yaml \
  --substitutions _TELEGRAM_TOKEN=${TELEGRAM_TOKEN},_OPENAI_API_KEY=${OPENAI_API_KEY}
```

### 3. Configure Webhook
After deployment, set the webhook:
```bash
curl -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/setWebhook" \
  -d "url=https://your-cloud-run-url.run.app/webhook"
```

## Dockerfile for Cloud Run
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "start.py"]
```

## Environment Variables Required
- TELEGRAM_TOKEN
- OPENAI_API_KEY  
- ASSISTANT_ID=asst_qgWQNNJGV0bGPy35Rdif4qpb
- ALLOWED_USERS=7668792787
- PORT=5000 (automatically set by Cloud Run)

## Post-Deployment Verification
1. Check webhook status: `curl https://api.telegram.org/bot${TOKEN}/getWebhookInfo`
2. Test bot response in Telegram
3. Monitor logs for successful message processing
4. Verify no polling conflicts in production

## Production Benefits
- Automatic webhook mode (no polling conflicts)
- Autoscaling based on demand
- Zero downtime deployments
- Built-in monitoring and logging
- HTTPS endpoint for webhook