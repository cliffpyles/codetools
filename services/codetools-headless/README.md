# Codetools Headless Service

## Overview

The Codetools Headless Service is designed to facilitate interaction with online content by providing a serverless solution for capturing web page screenshots and storing them for easy access. This service is ideal for archiving, content monitoring, and visual verification tasks.

## Services

### Screenshot Capture Service

This service enables users to capture and store screenshots of web pages in an S3 bucket, allowing for easy retrieval and use.

- **Caching**: Screenshots are stored in an S3 bucket, enabling quick access to previously captured images.
- **Security**: Utilizes AWS's secure environment to ensure that all operations and data storage are handled securely.

#### API Usage

**Endpoint**: `GET https://<APIGatewayURL>/screenshot`

**Query Parameters**:

- `url` (required): The URL of the web page to capture a screenshot of.
- `ratio` (optional): The device pixel ratio for the screenshot, affecting its quality.
- `force` (optional): Forces a new screenshot to be taken, even if one already exists for the specified URL.

**Example Request**:

```bash
curl "https://<APIGatewayURL>/screenshot?url=https://example.com&ratio=2&force=true"
```

### Deployment

#### Prerequisites

- **AWS SAM CLI**: Installed and configured ([Installation guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)).
- **Node.js**: Installed ([Node.js installation guide](https://nodejs.org/en/download/)).

#### Steps

1. **Prepare Your Environment**: Verify that Node.js and the AWS SAM CLI are installed and configured on your machine.

2. **Build Your Application**: Navigate to your project's root directory in a terminal and run:
   ```bash
   sam build
   ```

3. **Deploy Your Application**: Deploy your application using the SAM CLI's guided deployment process:
   ```bash
   sam deploy --guided
   ```
   Follow the prompts to complete the deployment, specifying your stack name, S3 bucket name, and any other required parameters when asked.
