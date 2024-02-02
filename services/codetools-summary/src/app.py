import os
import json
import boto3
from botocore.exceptions import ClientError
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
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


# Function to scrape and summarize content
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
            {"role": "user", "content": f"content to read:\n{text}"},
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


# Lambda handler
def lambda_handler(event, context):
    print(f"EVENT: {json.dumps(event)}")

    url = event["queryStringParameters"]["url"]
    print(f"URL: {json.dumps(url)}")

    # Check if summary exists in DynamoDB
    try:
        record = table.get_item(Key={"url": url})
        if "Item" in record:
            print(f"EXISTING SUMMARY: {json.dumps(record)}")
            return {"statusCode": 200, "body": record["Item"]["summary"]}
    except ClientError as e:
        print(e)

    # If not found, scrape, summarize, and store
    summarized_content = summarize_content(url)
    print(f"NEW SUMMARY: {json.dumps(summarized_content)}")

    item = {"url": url, **summarized_content}
    table.put_item(Item=item)

    return {"statusCode": 200, "body": summarized_content["summary"]}
