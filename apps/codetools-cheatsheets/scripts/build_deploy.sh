#!/bin/bash

# Define the project root directory and the path to the samconfig.toml file
PROJECT_ROOT=$(dirname "$0")/..
APP_DIR="$PROJECT_ROOT/app"
SAM_CONFIG="$PROJECT_ROOT/samconfig.toml"

# Attempt to extract the stack name from samconfig.toml
# Adjust the grep pattern based on your samconfig.toml structure
STACK_NAME=$(grep 'stack_name' "$SAM_CONFIG" | head -1 | awk -F'=' '{print $2}' | xargs | tr -d '"')

if [ -z "$STACK_NAME" ]; then
    echo "Failed to determine the CloudFormation stack name from samconfig.toml."
    exit 1
fi

echo "Determined stack name: $STACK_NAME"

# Fetch the S3 bucket name from CloudFormation stack outputs
BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)

if [ -z "$BUCKET_NAME" ]; then
    echo "Failed to fetch the S3 bucket name from CloudFormation stack outputs."
    exit 1
fi

echo "Deploying to bucket: $BUCKET_NAME"

# Build the app using Vite without changing the current directory
echo "Building the app..."
npm --prefix "$APP_DIR" run build

# Deploy the build to the S3 bucket without changing the current directory
echo "Deploying the app to S3..."
aws s3 sync "$APP_DIR/dist/" s3://"$BUCKET_NAME" --delete

echo "Deployment complete."
