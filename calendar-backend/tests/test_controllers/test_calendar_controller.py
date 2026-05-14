import pytest
from app import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "this-is-a-very-long-test-secret-key-1234567890"
    return app


@pytest.fixture
def client(app):
    return app.test_client()


DUMMY_ICS = b"BEGIN:VCALENDAR\nVERSION:2.0\nEND:VCALENDAR"


@patch("app.controllers.calendar_controller.service", autospec=True)
def test_generate_calendar_link_success(mock_service, client):
    mock_service.generate_subscription_link.return_value = "https://example.com/calendar.ics"

    response = client.post("/api/calendars/link", json={
        "base_url": "https://example.com",
        "ics_url": "https://example.com/source.ics",
        "method": "dictionary",
        "dictionary_id": 1,
        "user_mapping": {"hello": "👋"}
    })

    assert response.status_code == 200
    assert response.json["url"] == "https://example.com/calendar.ics"


def test_generate_calendar_link_invalid_schema(client):
    response = client.post("/api/calendars/link", json={})
    assert response.status_code == 400


@patch("app.controllers.calendar_controller.service", autospec=True)
def test_calendar_feed_success(mock_service, client):
    mock_service.generate_feed.return_value = DUMMY_ICS

    response = client.get("/api/calendars/feed?ics_url=a&method=dictionary")

    assert response.status_code == 200
    assert response.data == DUMMY_ICS
    assert response.mimetype == "text/calendar"
    assert "calendar.ics" in response.headers["Content-Disposition"]


def test_calendar_feed_missing_params(client):
    response = client.get("/api/calendars/feed")
    assert response.status_code == 400


@patch("app.controllers.calendar_controller.service", autospec=True)
def test_transform_calendar_success(mock_service, client):
    mock_service.transform_calendar.return_value = DUMMY_ICS

    response = client.post("/api/calendars/transform", json={
        "ics_url": "https://example.com/source.ics",
        "method": "dictionary",
        "dictionary_id": 1,
        "user_mapping": {"hello": "👋"}
    })

    assert response.status_code == 200
    assert response.data == DUMMY_ICS


def test_transform_calendar_invalid_schema(client):
    response = client.post("/api/calendars/transform", json={})
    assert response.status_code == 400


@patch("app.controllers.calendar_controller.service", autospec=True)
def test_transform_text_success(mock_service, client):
    mock_service.transform_text.return_value = "🔥"

    response = client.post("/api/calendars/transform-text", json={
        "text": "fire",
        "method": "dictionary",
        "dictionary_id": 1,
        "user_mapping": {"fire": "🔥"}
    })

    assert response.status_code == 200
    assert response.json["emoji"] == "🔥"


def test_transform_text_invalid_schema(client):
    response = client.post("/api/calendars/transform-text", json={})
    assert response.status_code == 400


def test_get_methods_success(client):
    response = client.get("/api/calendars/methods")

    assert response.status_code == 200
    assert "methods" in response.json
    assert "dictionary" in response.json["methods"]
