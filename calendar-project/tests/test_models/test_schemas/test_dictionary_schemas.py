import pytest
from marshmallow import ValidationError

from app.models.schemas.dictionary_schemas import (
    DictionaryEntrySchema,
    DictionaryEntryCreateSchema,
    DictionarySchema,
    DictionaryCreateSchema,
)

def test_dictionary_entry_schema_valid():
    schema = DictionaryEntrySchema()

    data = schema.load({
        "word": "hello",
        "emoji": "👋"
    })

    assert data["word"] == "hello"
    assert data["emoji"] == "👋"


def test_dictionary_entry_schema_invalid_word_length():
    schema = DictionaryEntrySchema()

    with pytest.raises(ValidationError):
        schema.load({"word": "", "emoji": "👋"})


def test_dictionary_entry_schema_invalid_emoji_length():
    schema = DictionaryEntrySchema()

    with pytest.raises(ValidationError):
        schema.load({"word": "hello", "emoji": "toolong"})


def test_dictionary_entry_create_schema_valid():
    schema = DictionaryEntryCreateSchema()

    data = schema.load({
        "word": "cat",
        "emoji": "🐱"
    })

    assert data["word"] == "cat"
    assert data["emoji"] == "🐱"


def test_dictionary_entry_create_schema_missing_fields():
    schema = DictionaryEntryCreateSchema()

    with pytest.raises(ValidationError):
        schema.load({"word": "cat"})


def test_dictionary_schema_valid():
    schema = DictionarySchema()

    data = schema.load({
        "name": "Emoji Dictionary",
        "language": "en",
        "description": "Test dictionary"
    })

    assert data["name"] == "Emoji Dictionary"
    assert data["language"] == "en"
    assert data["description"] == "Test dictionary"


def test_dictionary_schema_invalid_name_length():
    schema = DictionarySchema()

    with pytest.raises(ValidationError):
        schema.load({"name": "", "language": "en"})


def test_dictionary_schema_invalid_language_length():
    schema = DictionarySchema()

    with pytest.raises(ValidationError):
        schema.load({"name": "Valid", "language": ""})


def test_dictionary_create_schema_valid():
    schema = DictionaryCreateSchema()

    data = schema.load({
        "name": "Animals",
        "language": "en",
        "description": "Animal emojis"
    })

    assert data["name"] == "Animals"
    assert data["language"] == "en"
    assert data["description"] == "Animal emojis"


def test_dictionary_create_schema_optional_description():
    schema = DictionaryCreateSchema()

    data = schema.load({
        "name": "Food",
        "language": "en"
    })

    assert data["name"] == "Food"
    assert data["language"] == "en"
    assert "description" not in data or data["description"] is None


def test_dictionary_create_schema_invalid_name():
    schema = DictionaryCreateSchema()

    with pytest.raises(ValidationError):
        schema.load({"name": "", "language": "en"})
