# CodeTools-Summary Service

## Overview

CodeTools Summary is a service designed to summarize online content, making it easier for users to get the gist of web articles, blogs, and other textual content quickly. The service is accessible via a REST API and integrates with OpenAI's GPT for generating summaries.

## Features

- **Content Summarization**: Summarizes online articles and web pages.
- **Caching**: Stores summaries in DynamoDB for quick retrieval of previously summarized content.
- **Secure**: Utilizes AWS SSM for secure storage of sensitive information like API keys.

## API Usage

### Endpoint

`GET https://<apigatway_url>/prod/summary`

### Query Parameters

- `url` (required): The URL of the online content to summarize.
- `format` (optional): The format to return the response in (text, json, html)

### Example Request

```bash
curl "https://<apigatway_url>/prod/summary?format=html&url=https://example.com/article"
