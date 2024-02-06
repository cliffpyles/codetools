import os
import json
import markdown
from py_markdown_table.markdown_table import markdown_table
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


def render_json(content, status_code=200):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "body": json.dumps(content, indent=4),
    }


def render_markdown(content, status_code=200):
    body_content = markdown.markdown(
        content,
        extensions=[
            "sane_lists",
            "codehilite",
            "tables",
            "fenced_code",
            "def_list",
            "abbr",
            "pymdownx.blocks.details",
            "md_in_html",
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
            .grid {{
                display: grid;
                gap: 1em;
            }}
            .col-2 {{
                grid-template-columns: 1fr 1fr;
            }}
            .fz-xxs {{ font-size: 0.6rem; }}
            .fz-xs {{ font-size: 0.7rem; }}
            .fz-sm {{ font-size: 0.9rem; }}
            .fz-md {{ font-size: 1rem; }}
            .fz-lg {{ font-size: 1.1rem; }}
            .fz-xl {{ font-size: 1.2rem; }}
            .fz-xxl {{ font-size: 1.3rem; }}
        </style>
    </head>
    <body>
        <div class="markdown-body">
            {body_content}
        </div>
    </body>
</html>"""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": html_output,
    }


def render_text(content, status_code=200):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "text/plain; charset=utf-8"},
        "body": content,
    }


def render_response(item, item_key=None, format="text", status_code=200):
    content = item if item_key is None else item[item_key]

    if format == "text":
        return render_text(content, status_code)
    elif format == "html":
        return render_markdown(content, status_code)
    elif format == "json":
        return render_json(content, status_code)
    else:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": json.dumps({"error": "Unsupported format"}),
        }
