#!/bin/bash
# Enterprise IAM Setup Script for MartechEngine - PRODUCTION ONLY

set -euo pipefail

# --- Configuration ---
# Usage: ./gcp-setup-iam.sh <gcp-project-id>
PROJECT_ID="${1}"
ENVIRONMENT="production" # This script is hardcoded for production

SERVICE_ACCOUNT_NAME="martechengine-${ENVIRONMENT}-sa"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
SERVICE_ACCOUNT_DISPLAY_NAME="MartechEngine Production Service Account"

# --- Validation ---
if [[ -z "$PROJECT_ID" ]]; then
    echo "❌ Error: GCP Project ID is required."
    echo "Usage: $0 <gcp-project-id>"
    exit 1
fi

echo "🔐 Setting up PRODUCTION IAM for MartechEngine"
echo "   Project: $PROJECT_ID"
echo "   Service Acc: $SERVICE_ACCOUNT_EMAIL"
echo "--------------------------------------------------"

# 1. Create the Service Account
echo "🏗️  Step 1/3: Creating the service account..."
if gcloud iam service-accounts describe "$SERVICE_ACCOUNT_EMAIL" --project="$PROJECT_ID" &>/dev/null; then
    echo "   ✅ Service account '$SERVICE_ACCOUNT_NAME' already exists."
else
    gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
        --project="$PROJECT_ID" \
        --display-name="$SERVICE_ACCOUNT_DISPLAY_NAME"
    echo "   ✅ Service account created."
fi

# 2. Grant Required IAM Roles
echo "🔒 Step 2/3: Granting necessary IAM roles..."
ROLES=(
    "roles/secretmanager.secretAccessor"  # To read secrets
    "roles/cloudsql.client"             # To connect to Cloud SQL
    "roles/logging.logWriter"           # To write logs
    "roles/monitoring.metricWriter"     # To write metrics
    "roles/aiplatform.user"             # To use Vertex AI
    "roles/storage.objectViewer"        # To read from GCS buckets
)
for role in "${ROLES[@]}"; do
    echo "   - Granting role: $role"
    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
        --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
        --role="$role" \
        --condition=None > /dev/null
done
echo "   ✅ All roles granted."

# 3. Guidance on Key Management for CI/CD
echo "🔑 Step 3/3: Key Management Guidance for CI/CD..."
echo "   A service account key is required for your CI/CD pipeline to authenticate."
echo "   To create one and store it as a GitHub Secret, follow these steps:"
echo "   1. Create the key:"
echo "      gcloud iam service-accounts keys create ci-cd-key.json --iam-account=\"$SERVICE_ACCOUNT_EMAIL\" --project=\"$PROJECT_ID\""
echo "   2. Go to your GitHub repository -> Settings -> Secrets and variables -> Actions."
echo "   3. Create a new repository secret named 'GCP_SA_KEY'."
echo "   4. Copy the entire content of the 'ci-cd-key.json' file and paste it into the secret's value."
echo "   5. Securely DELETE the 'ci-cd-key.json' file from your local machine: rm ci-cd-key.json"
echo ""
echo "🎉 Enterprise IAM setup for PRODUCTION is complete!"
