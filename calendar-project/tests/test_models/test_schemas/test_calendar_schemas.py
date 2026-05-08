import pytest
from marshmallow import ValidationError

from app.models.schemas.calendar_schemas import (
    CalendarLinkSchema,
    CalendarTransformSchema,
    TransformTextSchema,
)

VALID_METHOD = "dictionary"
VALID_URL = "https://example.com/calendar.ics"

def test_calendar_link_schema_valid():
    schema = CalendarLinkSchema()

    data = schema.load({
        "base_url": "https://example.com",
        "ics_url": VALID_URL,
        "method": VALID_METHOD,
        "dictionary_id": 1,
        "user_mapping": {"meeting": "📅"}
    })

    assert data["base_url"] == "https://example.com"
    assert data["ics_url"] == VALID_URL
    assert data["method"] == VALID_METHOD
    assert data["dictionary_id"] == 1
    assert data["user_mapping"] == {"meeting": "📅"}


def test_calendar_link_schema_invalid_url():
    schema = CalendarLinkSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "base_url": "not-a-url",
            "ics_url": VALID_URL,
            "method": VALID_METHOD
        })


def test_calendar_link_schema_invalid_method():
    schema = CalendarLinkSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "base_url": "https://example.com",
            "ics_url": VALID_URL,
            "method": "invalid-method"
        })


def test_calendar_transform_schema_valid():
    schema = CalendarTransformSchema()

    data = schema.load({
        "ics_url": VALID_URL,
        "method": VALID_METHOD,
        "dictionary_id": None,
        "user_mapping": {"work": "💼"}
    })

    assert data["ics_url"] == VALID_URL
    assert data["method"] == VALID_METHOD
    assert data["dictionary_id"] is None
    assert data["user_mapping"] == {"work": "💼"}


def test_calendar_transform_schema_missing_required():
    schema = CalendarTransformSchema()

    with pytest.raises(ValidationError):
        schema.load({"method": VALID_METHOD})


def test_calendar_transform_schema_invalid_method():
    schema = CalendarTransformSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "ics_url": VALID_URL,
            "method": "invalid"
        })


# -----------------------------
# TransformTextSchema
# -----------------------------
def test_transform_text_schema_valid():
    schema = TransformTextSchema()

    data = schema.load({
        "text": "Meeting with team",
        "method": VALID_METHOD,
        "dictionary_id": 2,
        "user_mapping": {"meeting": "📅"}
    })

    assert data["text"] == "Meeting with team"
    assert data["method"] == VALID_METHOD
    assert data["dictionary_id"] == 2
    assert data["user_mapping"] == {"meeting": "📅"}


def test_transform_text_schema_invalid_text_length():
    schema = TransformTextSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "text": "",
            "method": VALID_METHOD
        })


def test_transform_text_schema_invalid_method():
    schema = TransformTextSchema()

    with pytest.raises(ValidationError):
        schema.load({
            "text": "Hello",
            "method": "invalid"
        })
