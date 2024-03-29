# Static Site

Template for a static site with CDN and access logging

## Features

- Hosting with S3
- CDN with CloudFront
- Access logs stored in separate S3 bucket

## Requirements

- [AWS CLI](https://aws.amazon.com/cli/)
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Cloud Resource Deployment

1. run `sam deploy --guided` (first time) or `sam deploy`

## Site Deployment

1. run `aws s3 sync ./site s3://<YOUR BUCKET NAME HERE>`
