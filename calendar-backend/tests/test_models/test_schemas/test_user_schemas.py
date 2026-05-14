import pytest
from marshmallow import ValidationError

from app.models.schemas.user_schemas import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
    LoginSchema,
)

def test_user_create_schema_normalization():
    schema = UserCreateSchema()

    data = schema.load({
        "username": "  DUY_123  ",
        "password": "  Abcdefg1  ",
        "confirm_password": "  Abcdefg1  "
    })

    assert data["username"] == "duy_123"
    assert data["password"] == "Abcdefg1"
    assert data["confirm_password"] == "Abcdefg1"


def test_user_create_schema_invalid_username_regex():
    schema = UserCreateSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "username": "Invalid Name!",
            "password": "Abcdefg1",
            "confirm_password": "Abcdefg1"
        })


def test_user_create_schema_invalid_password_regex():
    schema = UserCreateSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "username": "valid_user",
            "password": "abcdefg1",  # no uppercase
            "confirm_password": "abcdefg1"
        })


def test_user_create_schema_missing_fields():
    schema = UserCreateSchema()

    with pytest.raises(ValidationError):
        schema.load({})

def test_user_update_schema_normalization():
    schema = UserUpdateSchema()

    data = schema.load({
        "current_password": "  oldPass1  ",
        "new_password": "  NewPass1  ",
        "confirm_new_password": "  NewPass1  "
    })

    assert data["current_password"] == "oldPass1"
    assert data["new_password"] == "NewPass1"
    assert data["confirm_new_password"] == "NewPass1"


def test_user_update_schema_invalid_new_password():
    schema = UserUpdateSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "current_password": "oldPass1",
            "new_password": "weakpass",
            "confirm_new_password": "weakpass"
        })

def test_user_response_schema_dump():
    schema = UserResponseSchema()

    user = {
        "id": 1,
        "username": "duy",
        "is_admin": True
    }

    result = schema.dump(user)

    assert result["id"] == 1
    assert result["username"] == "duy"
    assert result["is_admin"] is True


def test_login_schema_normalization():
    schema = LoginSchema()

    data = schema.load({
        "username": "  DUY  ",
        "password": "  pass123  "
    })

    assert data["username"] == "duy"
    assert data["password"] == "pass123"


def test_login_schema_missing_fields():
    schema = LoginSchema()

    with pytest.raises(ValidationError):
        schema.load({"username": "duy"})
