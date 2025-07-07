# 🌍 Pinthenews - Google Cloud Run Deployment Guide

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud CLI** installed ([Install Guide](https://cloud.google.com/sdk/docs/install))
3. **Docker** installed and running
4. **Project** set up in Google Cloud Console

## Quick Setup

### 1. Install Google Cloud CLI (if not installed)
```bash
# macOS
brew install google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

### 2. Authenticate and Set Project
```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable Application Default Credentials
gcloud auth application-default login
```

### 3. One-Command Deployment
```bash
# Run the automated deployment script
./deploy.sh
```

## Manual Deployment Steps

### 1. Enable APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Create Secrets for API Keys
```bash
# Create secret for Anthropic API key
echo "your-anthropic-api-key" | gcloud secrets create anthropic-api-key --data-file=-

# Create secret for OpenAI API key (optional)
echo "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-
```

### 3. Build and Deploy
```bash
# Submit build using Cloud Build
gcloud builds submit --config cloudbuild.yaml

# Or build and deploy manually
docker build -t gcr.io/YOUR_PROJECT_ID/pinthenews .
docker push gcr.io/YOUR_PROJECT_ID/pinthenews

gcloud run deploy pinthenews \
  --image gcr.io/YOUR_PROJECT_ID/pinthenews \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --port 8080 \
  --max-instances 10
```

## Configuration Options

### Environment Variables
- `PORT`: Application port (default: 8080)
- `ANTHROPIC_API_KEY`: Required for AI functionality
- `OPENAI_API_KEY`: Optional for enhanced features

### Scaling Configuration
- **Memory**: 2Gi (adjustable based on needs)
- **CPU**: 2 cores (adjustable)
- **Max Instances**: 10 (prevents runaway costs)
- **Concurrency**: 100 requests per instance
- **Timeout**: 15 minutes for long-running operations

### Security Features
- Non-root user in container
- Secrets management for API keys
- CORS and XSRF protection enabled
- Health checks configured

## Monitoring and Management

### View Logs
```bash
gcloud run logs tail pinthenews --region us-central1
```

### Update Service
```bash
# Redeploy with new image
gcloud run deploy pinthenews --image gcr.io/YOUR_PROJECT_ID/pinthenews:latest
```

### Scale Service
```bash
# Update memory/CPU
gcloud run services update pinthenews \
  --memory 4Gi \
  --cpu 4 \
  --region us-central1
```

## Cost Optimization

- **Pay-per-use**: Only charged when requests are being processed
- **Auto-scaling**: Scales to zero when not in use
- **Resource limits**: Prevents unexpected charges
- **Regional deployment**: Choose closest region to users

## Troubleshooting

### Common Issues
1. **API not enabled**: Run `gcloud services enable` commands
2. **Missing secrets**: Ensure API keys are stored as secrets
3. **Build failures**: Check Dockerfile and dependencies
4. **Memory limits**: Increase memory allocation if needed

### Support
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Streamlit Cloud Deployment](https://docs.streamlit.io/deploy)
- [Google Cloud Console](https://console.cloud.google.com)

## Cost Estimate

**Typical usage (100 requests/day, 5 minutes per session):**
- Cloud Run: ~$5-10/month
- Container Registry: ~$1/month
- Secrets Manager: ~$1/month

**Total estimated cost: $7-12/month**

## Production Checklist

- [ ] Domain name configured (optional)
- [ ] SSL certificate (automatic with Cloud Run)
- [ ] Monitoring and alerting set up
- [ ] API key rotation plan
- [ ] Backup and disaster recovery
- [ ] Performance testing completed