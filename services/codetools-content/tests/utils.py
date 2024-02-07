import json
from app.utils import (
    render_json,
    render_markdown,
    render_text,
    render_response,
)


def test_render_json():
    content = {"key": "value"}
    response = render_json(content)
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == content
    assert response["headers"]["Content-Type"] == "application/json; charset=utf-8"


def test_render_markdown():
    content = "# Markdown Title"
    response = render_markdown(content)
    assert response["statusCode"] == 200
    assert "<h1>Markdown Title</h1>" in response["body"]
    assert response["headers"]["Content-Type"] == "text/html; charset=utf-8"


def test_render_text():
    content = "Just a simple text"
    response = render_text(content)
    assert response["statusCode"] == 200
    assert response["body"] == content
    assert response["headers"]["Content-Type"] == "text/plain; charset=utf-8"


def test_render_response_text():
    response = render_response("Simple text", format="text")
    assert response["statusCode"] == 200
    assert response["body"] == "Simple text"


def test_render_response_markdown():
    response = render_response("# Markdown", format="html")
    assert response["statusCode"] == 200
    assert "<h1>Markdown</h1>" in response["body"]


def test_render_response_json():
    response = render_response({"key": "value"}, format="json")
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"key": "value"}


def test_render_response_unsupported_format():
    response = render_response("content", format="xml")
    assert response["statusCode"] == 400
    assert json.loads(response["body"])["error"] == "Unsupported format"
