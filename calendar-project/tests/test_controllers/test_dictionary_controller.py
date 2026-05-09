import pytest
import io, json
from app import create_app
from app.exceptions import ForbiddenError, ValidationError, NotFoundError
from flask_jwt_extended import create_access_token
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


@pytest.fixture
def auth_header(app):
    with app.app_context():
        token = create_access_token(identity="1")
    return {"Authorization": f"Bearer {token}"}


class DummyDictionary:
    def __init__(self, id, name, language, description=None, entries=None):
        self.id = id
        self.name = name
        self.language = language
        self.description = description
        self.entries = entries or []


class DummyEntry:
    def __init__(self, id, word, emoji):
        self.id = id
        self.word = word
        self.emoji = emoji


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_get_all_dictionaries_success(mock_service, client, auth_header):
    mock_service.get_all_dictionaries.return_value = [
        DummyDictionary(1, "Animals", "EN")
    ]

    response = client.get("/api/dictionaries/")

    assert response.status_code == 200
    assert response.json[0]["name"] == "Animals"


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_get_dictionary_success(mock_service, client, auth_header):
    mock_service.get_dictionary.return_value = DummyDictionary(1, "Animals", "EN")

    response = client.get("/api/dictionaries/1", headers=auth_header)

    assert response.status_code == 200
    assert response.json["name"] == "Animals"


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_get_dictionary_not_found(mock_service, client, auth_header):
    mock_service.get_dictionary.side_effect = NotFoundError("Not found")

    response = client.get("/api/dictionaries/1")
    assert response.status_code == 404


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_create_dictionary_success(mock_service, client, auth_header):
    mock_service.create_dictionary.return_value = DummyDictionary(1, "NewDict", "EN")

    response = client.post("/api/dictionaries/", json={
        "name": "NewDict",
        "language": "EN"
    }, headers=auth_header)

    assert response.status_code == 201
    assert response.json["name"] == "NewDict"


def test_create_dictionary_invalid_schema(client, auth_header):
    response = client.post("/api/dictionaries/", json={}, headers=auth_header)
    assert response.status_code == 400


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_create_dictionary_validation_error(mock_service, client, auth_header):
    mock_service.create_dictionary.side_effect = ValidationError("Invalid")

    response = client.post("/api/dictionaries/", json={
        "name": "NewDict",
        "language": "EN"
    }, headers=auth_header)

    assert response.status_code == 400


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_delete_dictionary_success(mock_service, client, auth_header):
    response = client.delete("/api/dictionaries/1", headers=auth_header)

    assert response.status_code == 200
    assert response.json["message"] == "Dictionary deleted"


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_delete_dictionary_not_found(mock_service, client, auth_header):
    mock_service.delete_dictionary.side_effect = NotFoundError("Not found")

    response = client.delete("/api/dictionaries/1", headers=auth_header)
    assert response.status_code == 404


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_delete_dictionary_forbidden(mock_service, client, auth_header):
    mock_service.delete_dictionary.side_effect = ForbiddenError("Forbidden")

    response = client.delete("/api/dictionaries/1", headers=auth_header)
    assert response.status_code == 403


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_get_entries_success(mock_service, client, auth_header):
    mock_service.get_entries.return_value = [
        DummyEntry(1, "cat", "🐱")
    ]

    response = client.get("/api/dictionaries/1/entries", headers=auth_header)

    assert response.status_code == 200
    assert response.json[0]["word"] == "cat"


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_get_entries_not_found(mock_service, client, auth_header):
    mock_service.get_entries.side_effect = NotFoundError("Not found")

    response = client.get("/api/dictionaries/1/entries", headers=auth_header)
    assert response.status_code == 404


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_add_entry_success(mock_service, client, auth_header):
    mock_service.add_entry.return_value = DummyEntry(1, "dog", "🐶")

    response = client.post("/api/dictionaries/1/entries", json={
        "word": "dog",
        "emoji": "🐶"
    }, headers=auth_header)

    assert response.status_code == 201
    assert response.json["word"] == "dog"


def test_add_entry_invalid_schema(client, auth_header):
    response = client.post("/api/dictionaries/1/entries", json={}, headers=auth_header)
    assert response.status_code == 400


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_add_entry_not_found(mock_service, client, auth_header):
    mock_service.add_entry.side_effect = NotFoundError("Not found")

    response = client.post("/api/dictionaries/1/entries", json={
        "word": "dog",
        "emoji": "🐶"
    }, headers=auth_header)

    assert response.status_code == 404


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_delete_entry_success(mock_service, client, auth_header):
    response = client.delete("/api/dictionaries/1/entries/1", headers=auth_header)

    assert response.status_code == 200
    assert response.json["message"] == "Entry deleted"


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_delete_entry_not_found(mock_service, client, auth_header):
    mock_service.delete_entry.side_effect = NotFoundError("Not found")

    response = client.delete("/api/dictionaries/1/entries/1", headers=auth_header)
    assert response.status_code == 404


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_delete_entry_forbidden(mock_service, client, auth_header):
    mock_service.delete_entry.side_effect = ForbiddenError("Forbidden")

    response = client.delete("/api/dictionaries/1/entries/1", headers=auth_header)
    assert response.status_code == 403


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_bulk_insert_success(mock_service, client, auth_header):
    mock_service.bulk_insert_entries.return_value = 2

    response = client.post("/api/dictionaries/1/entries/bulk", json={
        "hello": "👋",
        "world": "🌍"
    }, headers=auth_header)

    assert response.status_code == 201
    assert response.json["inserted"] == 2


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_bulk_insert_invalid_schema(mock_service, client, auth_header):
    mock_service.bulk_insert_entries.side_effect = ValidationError("Entries must be a dictionary")

    response = client.post(
        "/api/dictionaries/1/entries/bulk",
        json="not-a-dict",
        headers=auth_header
    )
    assert response.status_code == 400


@patch("app.controllers.dictionary_controller.DictionaryService", spec=True)
def test_bulk_insert_not_found(mock_service, client, auth_header):
    mock_service.bulk_insert_entries.side_effect = NotFoundError("Not found")

    response = client.post("/api/dictionaries/1/entries/bulk", json={
        "hello": "👋"
    }, headers=auth_header)

    assert response.status_code == 404


@patch("app.controllers.calendar_controller.service", autospec=True)
def test_transform_file_success(mock_service, client):
    mock_service.transform_calendar_from_bytes.return_value = {
        "preview": "OK",
        "file": "BASE64DATA"
    }

    data = {
        "file": (io.BytesIO(b"BEGIN:VCALENDAR..."), "test.ics"),
        "method": "dictionary",
        "dictionary_id": "1",
        "user_mapping": json.dumps({"meeting": "📅"})
    }

    response = client.post(
        "/api/calendars/transform-file",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert response.json["preview"] == "OK"

    mock_service.transform_calendar_from_bytes.assert_called_once()


def test_transform_file_missing_file(client):
    data = {
        "method": "dictionary"
    }

    response = client.post(
        "/api/calendars/transform-file",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["message"] == "ICS file is required"


def test_transform_file_missing_method(client):
    data = {
        "file": (io.BytesIO(b"BEGIN:VCALENDAR..."), "test.ics")
    }

    response = client.post(
        "/api/calendars/transform-file",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["message"] == "Transformation method is required"