#!/bin/bash
# Pinthenews Google Cloud Run Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌍 Pinthenews Google Cloud Run Deployment${NC}"
echo "========================================"

# Check if required tools are installed
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud CLI not found. Please install it first:${NC}"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

# Get project ID
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}❌ No Google Cloud project set. Run: gcloud config set project YOUR_PROJECT_ID${NC}"
        exit 1
    fi
else
    PROJECT_ID=$GOOGLE_CLOUD_PROJECT
fi

echo -e "${GREEN}✅ Using project: $PROJECT_ID${NC}"

# Enable required APIs
echo -e "${YELLOW}Enabling required Google Cloud APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID
gcloud services enable run.googleapis.com --project=$PROJECT_ID
gcloud services enable containerregistry.googleapis.com --project=$PROJECT_ID

# Set region
REGION=${REGION:-us-central1}
echo -e "${GREEN}✅ Using region: $REGION${NC}"

# Check for environment file
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found. Please create it with your API keys.${NC}"
    exit 1
fi

# Create secrets for API keys
echo -e "${YELLOW}Creating secrets for API keys...${NC}"

# Extract API keys from .env file
ANTHROPIC_API_KEY=$(grep "ANTHROPIC_API_KEY=" .env | cut -d '=' -f2)
OPENAI_API_KEY=$(grep "OPENAI_API_KEY=" .env | cut -d '=' -f2)

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}❌ ANTHROPIC_API_KEY not found in .env file${NC}"
    exit 1
fi

# Create secrets
echo "$ANTHROPIC_API_KEY" | gcloud secrets create anthropic-api-key --data-file=- --project=$PROJECT_ID 2>/dev/null || \
echo "$ANTHROPIC_API_KEY" | gcloud secrets versions add anthropic-api-key --data-file=- --project=$PROJECT_ID

if [ ! -z "$OPENAI_API_KEY" ]; then
    echo "$OPENAI_API_KEY" | gcloud secrets create openai-api-key --data-file=- --project=$PROJECT_ID 2>/dev/null || \
    echo "$OPENAI_API_KEY" | gcloud secrets versions add openai-api-key --data-file=- --project=$PROJECT_ID
fi

echo -e "${GREEN}✅ Secrets created${NC}"

# Build and deploy using Cloud Build
echo -e "${YELLOW}Building and deploying with Cloud Build...${NC}"

# Update service.yaml with project ID
sed "s/PROJECT_ID/$PROJECT_ID/g" service.yaml > service-deployed.yaml

# Submit build
gcloud builds submit --config cloudbuild.yaml --project=$PROJECT_ID

echo -e "${GREEN}✅ Build completed${NC}"

# Get the service URL
SERVICE_URL=$(gcloud run services describe pinthenews --region=$REGION --project=$PROJECT_ID --format="value(status.url)" 2>/dev/null)

if [ ! -z "$SERVICE_URL" ]; then
    echo -e "${GREEN}🚀 Deployment successful!${NC}"
    echo -e "${GREEN}🌐 Your app is live at: $SERVICE_URL${NC}"
    echo ""
    echo -e "${BLUE}📋 Deployment Summary:${NC}"
    echo "• Project: $PROJECT_ID"
    echo "• Region: $REGION"  
    echo "• Service: pinthenews"
    echo "• URL: $SERVICE_URL"
    echo ""
    echo -e "${YELLOW}📝 Next steps:${NC}"
    echo "• Test your application at the URL above"
    echo "• Monitor logs: gcloud run logs tail pinthenews --region=$REGION"
    echo "• View metrics in Google Cloud Console"
else
    echo -e "${RED}❌ Deployment failed. Check the logs above.${NC}"
    exit 1
fi