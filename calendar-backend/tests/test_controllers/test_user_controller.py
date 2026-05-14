import pytest
from app import create_app
from app.exceptions import ForbiddenError, ValidationError
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

class DummyUser:
    def __init__(self, id, username, is_admin=False):
        self.id = id
        self.username = username
        self.is_admin = is_admin



@patch("app.controllers.user_controller.UserService", spec=True)
def test_get_users_success(mock_service, client, auth_header):
    mock_service.get_user.return_value = DummyUser(1, "admin", True)
    mock_service.get_users.return_value = [DummyUser(1, "duy", True)]

    response = client.get("/api/users/", headers=auth_header)

    assert response.status_code == 200
    assert response.json[0]["username"] == "duy"


def test_get_users_missing_jwt(client):
    response = client.get("/api/users/")
    assert response.status_code == 401


def test_get_users_invalid_jwt(client):
    response = client.get("/api/users/", headers={"Authorization": "Bearer invalid"})
    assert response.status_code in (401, 422)


@patch("app.controllers.user_controller.UserService", spec=True)
def test_get_users_admin_check_forbidden(mock_service, client, auth_header):
    mock_service.get_user.return_value = DummyUser(1, "duy", False)
    mock_service.assert_admin.side_effect = ForbiddenError("Not admin")

    response = client.get("/api/users/", headers=auth_header)
    assert response.status_code == 403


@patch("app.controllers.user_controller.UserService", spec=True)
def test_create_user_service_validation_error(mock_service, client):
    mock_service.create_user.side_effect = ValidationError("Invalid")

    response = client.post("/api/users/", json={
        "username": "duy",
        "password": "Password1",
        "confirm_password": "Password1"
    })

    assert response.status_code == 400


@patch("app.controllers.user_controller.UserService", spec=True)
def test_create_user_success(mock_service, client):
    mock_service.create_user.return_value = DummyUser(1, "duy", False)

    response = client.post("/api/users/", json={
        "username": "duy",
        "password": "Password1",
        "confirm_password": "Password1"
    })

    assert response.status_code == 201
    assert response.json["username"] == "duy"
    assert "access_token" in response.json


def test_create_user_invalid_schema(client):
    response = client.post("/api/users/", json={"username": "duy"})
    assert response.status_code == 400


@patch("app.controllers.user_controller.UserService", spec=True)
def test_set_admin_success(mock_service, client, auth_header):
    mock_service.make_admin.return_value = DummyUser(2, "bob", True)

    response = client.put("/api/users/2/admin", headers=auth_header)

    assert response.status_code == 200
    assert response.json["is_admin"] is True


@patch("app.controllers.user_controller.UserService", spec=True)
def test_set_admin_forbidden(mock_service, client, auth_header):
    mock_service.make_admin.side_effect = ForbiddenError("Forbidden")

    response = client.put("/api/users/2/admin", headers=auth_header)
    assert response.status_code == 403


@patch("app.controllers.user_controller.UserService", spec=True)
def test_update_password_success(mock_service, client, auth_header):
    mock_service.update_user_password.return_value = DummyUser(1, "duy", False)

    response = client.put("/api/users/1/password", json={
        "current_password": "OldPass1",
        "new_password": "NewPass1",
        "confirm_new_password": "NewPass1"
    }, headers=auth_header)

    assert response.status_code == 200
    assert response.json["username"] == "duy"


def test_update_password_invalid_schema(client, auth_header):
    response = client.put("/api/users/1/password", json={}, headers=auth_header)
    assert response.status_code == 400


@patch("app.controllers.user_controller.UserService", spec=True)
def test_update_password_wrong_current(mock_service, client, auth_header):
    mock_service.update_user_password.side_effect = ForbiddenError("Wrong password")

    response = client.put("/api/users/1/password", json={
        "current_password": "wrong",
        "new_password": "NewPass1",
        "confirm_new_password": "NewPass1"
    }, headers=auth_header)

    assert response.status_code == 403


@patch("app.controllers.user_controller.UserService", spec=True)
def test_delete_user_success(mock_service, client, auth_header):
    response = client.delete("/api/users/1", headers=auth_header)

    assert response.status_code == 200
    assert response.json["message"] == "Deleted"


@patch("app.controllers.user_controller.UserService", spec=True)
def test_delete_user_forbidden(mock_service, client, auth_header):
    mock_service.delete_user.side_effect = ForbiddenError("Forbidden")

    response = client.delete("/api/users/1", headers=auth_header)
    assert response.status_code == 403


@patch("app.controllers.user_controller.UserService", spec=True)
def test_login_success(mock_service, client):
    mock_service.authenticate.return_value = DummyUser(1, "duy", False)

    response = client.post("/api/users/login", json={
        "username": "duy",
        "password": "Password1"
    })

    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_invalid_schema(client):
    response = client.post("/api/users/login", json={"username": "duy"})
    assert response.status_code == 400


@patch("app.controllers.user_controller.UserService", spec=True)
def test_me_success(mock_service, client, auth_header):
    mock_service.get_user.return_value = DummyUser(1, "duy", False)

    response = client.get("/api/users/me", headers=auth_header)

    assert response.status_code == 200
    assert response.json["username"] == "duy"
