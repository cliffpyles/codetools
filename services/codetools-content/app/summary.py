import os
import json
import boto3
from botocore.exceptions import ClientError
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from .utils import get_openai_api_key, render_response
from .prompts import SYSTEM_CONTEXT, SUMMARY_PROMPT

# Initialize clients
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


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
        model="gpt-4-turbo-preview",
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


def handler(event, context):
    print(f"EVENT: {json.dumps(event)}")

    url = event["queryStringParameters"].get("url")
    print(f"URL: {json.dumps(url)}")
    response_format = event["queryStringParameters"].get("format", "text").lower()
    print(f"FORMAT: {response_format}")
    force = event["queryStringParameters"].get("force", False)
    print(f"FORCE: {force}")

    if force is False:
        try:
            record = table.get_item(Key={"url": url})
            if "Item" in record:
                print(f"EXISTING SUMMARY: {json.dumps(record)}")
                return render_response(
                    record["Item"], item_key="summary", format=response_format
                )
        except ClientError as e:
            print(e)

    summarized_content = summarize_content(url)
    print(f"NEW SUMMARY: {json.dumps(summarized_content)}")

    item = {"url": url, **summarized_content}
    table.put_item(Item=item)

    return render_response(
        summarized_content, item_key="summary", format=response_format
    )
