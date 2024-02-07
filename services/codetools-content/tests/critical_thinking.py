import json
import pytest
import requests_mock
from unittest.mock import patch, MagicMock
from app.critical_thinking import analyze_content, handle_render


@pytest.fixture
def mock_openai_response():
    """Fixture to mock OpenAI API response."""
    return {
        "choices": [
            {
                "message": {
                    "content": json.dumps(
                        {
                            "paragraphs": [
                                {
                                    "content": "Test paragraph",
                                    "biases": [
                                        {
                                            "name": "Bias Name",
                                            "description": "Bias Description",
                                            "explanation": "Bias Explanation",
                                        }
                                    ],
                                    "fallacies": [
                                        {
                                            "name": "Fallacy Name",
                                            "description": "Fallacy Description",
                                            "explanation": "Fallacy Explanation",
                                        }
                                    ],
                                }
                            ]
                        }
                    )
                }
            }
        ]
    }


@pytest.fixture
def mock_web_page():
    """Fixture to return mock HTML content for web scraping."""
    return """
    <html>
        <head>
            <title>Test Title</title>
            <meta name="author" content="Test Author">
            <meta property="article:published_time" content="Test Date">
            <meta property="article:section" content="Test Category">
        </head>
        <body>
            Test Content
        </body>
    </html>
    """


@pytest.fixture
def monkeypatch_env(monkeypatch):
    """Fixture to mock environment variables."""
    monkeypatch.setenv("DYNAMODB_TABLE", "test_table")


def disable_test_analyze_content(
    requests_mock, mock_openai_response, mock_web_page, monkeypatch_env
):
    url = "http://test.com"
    # text = mock_openai_response()
    requests_mock.get(url, text=mock_web_page)

    # Ensure the patch is applied to the correct import path
    with patch(
        "app.critical_thinking.get_openai_api_key", return_value="test_api_key"
    ), patch("app.critical_thinking.OpenAI") as mock_openai:
        mock_client = mock_openai(api_key="test_api_key")
        mock_client.chat.completions.create.return_value = mock_openai_response

        result = analyze_content(url)
        assert result["title"] == "Test Title"
        assert result["author"] == "Test Author"
        assert result["publish_date"] == "Test Date"
        assert result["categories"] == ["Test Category"]
        assert "paragraphs" in result["analysis"]


def test_handle_render_html():
    content = {
        "analysis": {
            "paragraphs": [
                {
                    "content": "Test paragraph",
                    "biases": [
                        {
                            "name": "Bias Name",
                            "description": "Bias Description",
                            "explanation": "Bias Explanation",
                        }
                    ],
                    "fallacies": [
                        {
                            "name": "Fallacy Name",
                            "description": "Fallacy Description",
                            "explanation": "Fallacy Explanation",
                        }
                    ],
                }
            ]
        }
    }
    response = handle_render(content, format="html")
    assert response["statusCode"] == 200
    assert "Test paragraph" in response["body"]
    assert "Bias Name" in response["body"]
    assert "Fallacy Name" in response["body"]


def test_handle_render_non_html():
    content = {"key": "value"}
    response = handle_render(content, format="json")
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == content


# Ensure pytest is installed and run the tests with the following command:
# pytest test_critical_thinking.py
