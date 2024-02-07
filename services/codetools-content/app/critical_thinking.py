import os
import simplejson as json
import boto3
from botocore.exceptions import ClientError
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from .utils import get_openai_api_key, render_response
from .prompts import CRITICAL_THINKING_CONTEXT


def analyze_content(url):
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
                "content": CRITICAL_THINKING_CONTEXT,
            },
            {"role": "user", "content": f"url:\n{url}\n\ncontent:\n{text}"},
        ],
        temperature=0,
    )
    content = completion.choices[0].message.content.strip()
    print(f"CONTENT: {content}")
    parsed_content = json.loads(content)

    return {
        "title": title,
        "author": author,
        "publish_date": publish_date,
        "categories": categories,
        "analysis": parsed_content,
    }


def handle_render(content, format="html"):
    if format != "html":
        return render_response(content, format=format)

    analyzed_paragraphs = []

    for paragraph in content.get("analysis").get("paragraphs"):
        bias_count = len(paragraph.get("biases", []))
        fallacy_count = len(paragraph.get("fallacies", []))
        biases = [
            f"**{bias['name']}**: {bias['description']}\n\nReasoning: {bias['explanation']}"
            for bias in paragraph.get("biases", [])
        ]
        fallacies = [
            f"**{fallacy['name']}**: {fallacy['description']}\n\nReasoning: {fallacy['explanation']}"
            for fallacy in paragraph.get("fallacies", [])
        ]
        bias_content = "\n\n".join(biases)
        fallacy_content = "\n\n".join(fallacies)
        paragraph_section = (
            f"\n<div markdown='1' class='grid col-2'>\n{paragraph.get('content', '')}"
        )
        paragraph_section = f"{paragraph_section}\n<div markdown='1' class='fz-xs'>"
        if bias_count > 0:
            bias_details = f"""
/// details | Biases ({bias_count})
    type: warning

{bias_content}
///
""".strip()
            paragraph_section = f"{paragraph_section}\n\n{bias_details}"

        if fallacy_count > 0:
            fallacy_details = f"""
/// details | Fallacies ({fallacy_count})
    type: warning

{fallacy_content}
///
""".strip()
            paragraph_section = f"{paragraph_section}\n\n{fallacy_details}"
        paragraph_section = f"{paragraph_section}\n</div>\n</div>"
        analyzed_paragraphs.append(paragraph_section)

    markdown_content = "\n\n".join(analyzed_paragraphs)

    return render_response(markdown_content, format="html")


def handler(event, context):
    print(f"EVENT: {json.dumps(event)}")

    url = event["queryStringParameters"].get("url")
    print(f"URL: {json.dumps(url)}")
    force = event["queryStringParameters"].get("force", False)
    print(f"FORCE: {force}")
    format = event["queryStringParameters"].get("format", "html")
    print(f"FORMAT: {format}")

    # Initialize clients
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    if not force:
        try:
            record = table.get_item(Key={"url": url})
            if "Item" in record:
                print(f"EXISTING ANALYSIS: {json.dumps(record)}")

                return handle_render(record["Item"], format=format)
        except ClientError as e:
            print(e)

    analyzed_content = analyze_content(url)
    print(f"NEW ANALYSIS: {json.dumps(analyzed_content)}")

    item = {"url": url, **analyzed_content}
    table.put_item(Item=item)

    return handle_render(analyze_content, format=format)
