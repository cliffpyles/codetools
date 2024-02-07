# Codetools Content Services

## Overview

Codetools content services provide tools for enhanced interaction with online content, focusing on analysis and insight generation.

## Services

### Content Summarization Service

This service offers concise summaries of online articles and web pages, highlighting main points and essential information.

- **Caching**: Efficiently retrieves previously summarized content from DynamoDB.
- **Security**: Securely stores sensitive information, like API keys, using AWS SSM.

#### API Usage

**Endpoint**: `GET https://<DomainName>/summary`

**Query Parameters**:

- `url` (required): The URL of the content you want to summarize.
- `format` (optional): Specifies the response format (text, JSON, HTML).
- `force` (optional): Ignores the cache to generate a new summary.

**Example Request**:

```bash
curl "https://<DomainName>/summary?format=html&url=https://example.com/article"
```

### Critical Thinking Service

Analyzes content for logical fallacies and biases, providing a detailed breakdown to help you evaluate the reliability and objectivity of information.

- **Caching**: Stores analysis results in DynamoDB for quick retrieval.
- **Flexible Output**: Delivers rich presentation of analysis results in HTML format, including identified biases and fallacies.

#### API Usage

**Endpoint**: `GET https://<DomainName>/critical-thinking`

**Query Parameters**:

- `url` (required): The URL of the content to analyze.
- `format` (optional): The response format, defaulting to HTML.
- `force` (optional): Generates a new analysis, bypassing any cached data.

**Example Request**:

```bash
curl "https://<DomainName>/critical-thinking?format=html&url=https://example.com/article"
```

### Deployment

#### Prerequisites

- **AWS SAM CLI**: Installed and configured ([Installation guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)).
- **Python 3**: Installed ([Python installation guide](https://www.python.org/downloads/)).
- **ACM Certificate**: For your domain ([AWS ACM documentation](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)).
- **Hosted Zone in AWS Route 53**: For your domain ([AWS Route 53 documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)).

#### Steps

1. **Prepare Your Environment**: Verify that Python 3 and the AWS SAM CLI are installed and configured on your machine.

2. **Build Your Application**: Navigate to your project's root directory in a terminal and run:
   ```bash
   sam build
   ```

3. **Deploy Your Application**: Deploy your application using the SAM CLI's guided deployment process:
   ```bash
   sam deploy --guided
   ```
   Follow the prompts to complete the deployment, specifying your stack name, domain name, ACM certificate ARN, and hosted zone ID when asked.

