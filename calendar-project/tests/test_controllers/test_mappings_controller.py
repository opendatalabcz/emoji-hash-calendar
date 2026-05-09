import pytest
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


class DummySet:
    def __init__(self, id, name, mappings=None):
        self.id = id
        self.name = name
        self.mappings = mappings or []


class DummyMapping:
    def __init__(self, id, word, emoji):
        self.id = id
        self.word = word
        self.emoji = emoji


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_get_sets_success(mock_service, client, auth_header):
    mock_service.get_user_sets.return_value = [
        DummySet(1, "Animals", [DummyMapping(1, "cat", "🐱")])
    ]

    response = client.get("/api/mappings/sets", headers=auth_header)

    assert response.status_code == 200
    assert response.json[0]["name"] == "Animals"


def test_get_sets_missing_jwt(client):
    response = client.get("/api/mappings/sets")
    assert response.status_code == 401


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_create_set_success(mock_service, client, auth_header):
    mock_service.create_set.return_value = DummySet(1, "New Set")

    response = client.post("/api/mappings/sets", json={"name": "New Set"}, headers=auth_header)

    assert response.status_code == 201
    assert response.json["name"] == "New Set"


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_create_set_validation_error(mock_service, client, auth_header):
    mock_service.create_set.side_effect = ValidationError("Invalid")

    response = client.post("/api/mappings/sets", json={"name": "New Set"}, headers=auth_header)

    assert response.status_code == 400


def test_create_set_invalid_schema(client, auth_header):
    response = client.post("/api/mappings/sets", json={}, headers=auth_header)
    assert response.status_code == 400


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_delete_set_success(mock_service, client, auth_header):
    response = client.delete("/api/mappings/sets/1", headers=auth_header)

    assert response.status_code == 200
    assert response.json["message"] == "Deleted"


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_delete_set_forbidden(mock_service, client, auth_header):
    mock_service.delete_set.side_effect = ForbiddenError("Forbidden")

    response = client.delete("/api/mappings/sets/1", headers=auth_header)
    assert response.status_code == 403


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_delete_set_not_found(mock_service, client, auth_header):
    mock_service.delete_set.side_effect = NotFoundError("Not found")

    response = client.delete("/api/mappings/sets/1", headers=auth_header)
    assert response.status_code == 404


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_update_set_success(mock_service, client, auth_header):
    mock_service.update_set.return_value = DummySet(1, "Updated", [])

    response = client.put("/api/mappings/sets/1", json={
        "name": "Updated",
        "mappings": []
    }, headers=auth_header)

    assert response.status_code == 200
    assert response.json["name"] == "Updated"


def test_update_set_invalid_schema(client, auth_header):
    response = client.put("/api/mappings/sets/1", json={}, headers=auth_header)
    assert response.status_code == 400


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_update_set_not_found(mock_service, client, auth_header):
    mock_service.update_set.side_effect = NotFoundError("Not found")

    response = client.put("/api/mappings/sets/1", json={
        "name": "Updated",
        "mappings": []
    }, headers=auth_header)

    assert response.status_code == 404


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_get_mappings_success(mock_service, client, auth_header):
    mock_service.get_mappings.return_value = [
        DummyMapping(1, "cat", "🐱")
    ]

    response = client.get("/api/mappings/sets/1/mappings", headers=auth_header)

    assert response.status_code == 200
    assert response.json[0]["word"] == "cat"


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_get_mappings_not_found(mock_service, client, auth_header):
    mock_service.get_mappings.side_effect = NotFoundError("Not found")

    response = client.get("/api/mappings/sets/1/mappings", headers=auth_header)
    assert response.status_code == 404


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_create_mapping_success(mock_service, client, auth_header):
    mock_service.create_mapping.return_value = DummyMapping(1, "dog", "🐶")

    response = client.post("/api/mappings/sets/1/mappings", json={
        "word": "dog",
        "emoji": "🐶"
    }, headers=auth_header)

    assert response.status_code == 201
    assert response.json["word"] == "dog"


def test_create_mapping_invalid_schema(client, auth_header):
    response = client.post("/api/mappings/sets/1/mappings", json={}, headers=auth_header)
    assert response.status_code == 400


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_create_mapping_not_found(mock_service, client, auth_header):
    mock_service.create_mapping.side_effect = NotFoundError("Not found")

    response = client.post("/api/mappings/sets/1/mappings", json={
        "word": "dog",
        "emoji": "🐶"
    }, headers=auth_header)

    assert response.status_code == 404


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_delete_mapping_success(mock_service, client, auth_header):
    response = client.delete("/api/mappings/mappings/1", headers=auth_header)

    assert response.status_code == 200
    assert response.json["message"] == "Deleted"


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_delete_mapping_forbidden(mock_service, client, auth_header):
    mock_service.delete_mapping.side_effect = ForbiddenError("Forbidden")

    response = client.delete("/api/mappings/mappings/1", headers=auth_header)
    assert response.status_code == 403


@patch("app.controllers.mappings_controller.MappingService", spec=True)
def test_delete_mapping_not_found(mock_service, client, auth_header):
    mock_service.delete_mapping.side_effect = NotFoundError("Not found")

    response = client.delete("/api/mappings/mappings/1", headers=auth_header)
    assert response.status_code == 404
