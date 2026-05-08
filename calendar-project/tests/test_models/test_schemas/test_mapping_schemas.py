import pytest
from marshmallow import ValidationError

from app.models.schemas.mapping_schemas import (
    MappingSchema,
    MappingCreateSchema,
    MappingSetSchema,
    MappingSetCreateSchema,
)

def test_mapping_schema_valid():
    schema = MappingSchema()

    data = schema.load({
        "word": "hello",
        "emoji": "👋"
    })

    assert data["word"] == "hello"
    assert data["emoji"] == "👋"


def test_mapping_schema_invalid_word():
    schema = MappingSchema()

    with pytest.raises(ValidationError):
        schema.load({"word": "", "emoji": "👋"})


def test_mapping_schema_invalid_emoji_length():
    schema = MappingSchema()

    with pytest.raises(ValidationError):
        schema.load({"word": "hello", "emoji": "toolong"})

def test_mapping_create_schema_valid():
    schema = MappingCreateSchema()

    data = schema.load({
        "word": "cat",
        "emoji": "🐱"
    })

    assert data["word"] == "cat"
    assert data["emoji"] == "🐱"


def test_mapping_create_schema_missing_fields():
    schema = MappingCreateSchema()

    with pytest.raises(ValidationError):
        schema.load({"word": "cat"})

def test_mapping_set_schema_valid_nested():
    schema = MappingSetSchema()

    data = schema.load({
        "name": "Animals",
        "mappings": [
            {"word": "dog", "emoji": "🐶"},
            {"word": "cat", "emoji": "🐱"}
        ]
    })

    assert data["name"] == "Animals"
    assert len(data["mappings"]) == 2
    assert data["mappings"][0]["word"] == "dog"


def test_mapping_set_schema_invalid_nested():
    schema = MappingSetSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "name": "Animals",
            "mappings": [
                {"word": "", "emoji": "🐶"}  # invalid
            ]
        })

def test_mapping_set_create_schema_valid():
    schema = MappingSetCreateSchema()

    data = schema.load({
        "name": "My Set",
        "mappings": [
            {"word": "sun", "emoji": "☀️"}
        ]
    })

    assert data["name"] == "My Set"
    assert len(data["mappings"]) == 1


def test_mapping_set_create_schema_name_length():
    schema = MappingSetCreateSchema()

    with pytest.raises(ValidationError):
        schema.load({"name": "ab"})  # too short


def test_mapping_set_create_schema_optional_mappings():
    schema = MappingSetCreateSchema()

    data = schema.load({"name": "Valid Name"})

    assert data["name"] == "Valid Name"
    assert "mappings" not in data or data["mappings"] == []
