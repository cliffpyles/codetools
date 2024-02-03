import os
import json
import boto3
from botocore.exceptions import ClientError
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import markdown

from .prompts import SYSTEM_CONTEXT, SUMMARY_PROMPT

# Initialize clients
dynamodb = boto3.resource("dynamodb")
ssm = boto3.client("ssm")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


# Fetch OpenAI API key from SSM
def get_openai_api_key():
    try:
        response = ssm.get_parameter(
            Name=os.environ["OPENAI_API_KEY_SSM_NAME"], WithDecryption=True
        )
        return response["Parameter"]["Value"]
    except ClientError as e:
        print(e)
        return None


# Scrape and summarize content
def summarize_content(url):
    # Scrape content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract text for summarization
    text = soup.get_text()

    # Extract additional fields
    title = soup.find("title").text if soup.find("title") else "No Title Found"
    author = (
        soup.find("meta", attrs={"name": "author"})["content"]
        if soup.find("meta", attrs={"name": "author"})
        else "Author Unknown"
    )
    publish_date = (
        soup.find("meta", attrs={"property": "article:published_time"})["content"]
        if soup.find("meta", attrs={"property": "article:published_time"})
        else "Publish Date Unknown"
    )
    categories = (
        [
            meta["content"]
            for meta in soup.find_all("meta", attrs={"property": "article:section"})
        ]
        if soup.find_all("meta", attrs={"property": "article:section"})
        else ["No Categories"]
    )

    # Summarize content using OpenAI
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_CONTEXT,
            },
            {"role": "user", "content": f"url:\n{url}\n\ncontent to read:\n{text}"},
            {
                "role": "user",
                "content": SUMMARY_PROMPT,
            },
        ],
        temperature=0,
    )

    summary = completion.choices[0].message.content.strip()

    return {
        "title": title,
        "author": author,
        "publish_date": publish_date,
        "categories": categories,
        "summary": summary,
    }


def render_html(content):
    body_content = markdown.markdown(
        content,
        extensions=[
            "sane_lists",
            "codehilite",
            "tables",
            "fenced_code",
            "def_list",
            "abbr",
        ],
        output_format="html",
    )
    html_output = f"""<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.0/github-markdown.min.css">
        <style>
            .markdown-body {{
                box-sizing: border-box;
                min-width: 200px;
                max-width: 980px;
                margin: 0 auto;
                padding: 45px;
            }}
        </style>
    </head>
    <body>
        <div class="markdown-body">
            {body_content}
        </div>
    </body>
</html>"""

    return html_output


# Render content
def render_response(summarized_content, response_format, status_code=200):
    if response_format == "text":
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": summarized_content["summary"],
        }
    elif response_format == "html":
        html_response = render_html(summarized_content["summary"])

        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": html_response,
        }
    elif response_format == "json":
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": json.dumps(summarized_content),
        }
    else:
        # Handle unsupported formats by defaulting to an error in JSON format
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": json.dumps({"error": "Unsupported format"}),
        }


# Lambda handler
def lambda_handler(event, context):
    print(f"EVENT: {json.dumps(event)}")

    url = event["queryStringParameters"].get("url")
    print(f"URL: {json.dumps(url)}")
    response_format = event["queryStringParameters"].get("format", "text").lower()
    print(f"FORMAT: {response_format}")

    # Check if summary exists in DynamoDB
    try:
        record = table.get_item(Key={"url": url})
        if "Item" in record:
            print(f"EXISTING SUMMARY: {json.dumps(record)}")
            return render_response(record["Item"], response_format)
    except ClientError as e:
        print(e)

    # If not found, scrape, summarize, and store
    summarized_content = summarize_content(url)
    print(f"NEW SUMMARY: {json.dumps(summarized_content)}")

    item = {"url": url, **summarized_content}
    table.put_item(Item=item)

    return render_response(summarized_content, response_format)
