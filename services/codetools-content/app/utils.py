import os
import json
import markdown
import boto3
from botocore.exceptions import ClientError

ssm = boto3.client("ssm")


def get_openai_api_key():
    try:
        response = ssm.get_parameter(
            Name=os.environ["OPENAI_API_KEY_SSM_NAME"], WithDecryption=True
        )
        return response["Parameter"]["Value"]
    except ClientError as e:
        print(e)
        return None


def render_markdown(content):
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


def render_response(item, item_key, format, status_code=200):
    if format == "text":
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "text/plain; charset=utf-8"},
            "body": item[item_key],
        }
    elif format == "html":
        html_response = render_markdown(item[item_key])

        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": html_response,
        }
    elif format == "json":
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": json.dumps(item),
        }
    else:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": json.dumps({"error": "Unsupported format"}),
        }
