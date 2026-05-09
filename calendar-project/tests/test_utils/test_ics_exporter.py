import pytest
from io import BytesIO
from datetime import datetime
from app.exporters.ics_exporter import ICSExporter
from app.exceptions import ValidationError, AppException


class DummyEvent:
    """Simple dummy event matching the attributes used by ICSExporter."""
    def __init__(
        self,
        emoji,
        start,
        end,
        uid="123",
        status="CONFIRMED",
        created=None,
        last_modified=None,
        is_all_day=False
    ):
        self.emoji = emoji
        self.start = start
        self.end = end
        self.uid = uid
        self.status = status
        self.created = created
        self.last_modified = last_modified
        self.is_all_day = is_all_day


def test_export_stream_success():
    exporter = ICSExporter()
    output = BytesIO()

    event = DummyEvent(
        emoji="🔥",
        start=datetime(2024, 1, 1, 10, 0),
        end=datetime(2024, 1, 1, 11, 0)
    )

    exporter.export_stream(output, [event])

    data = output.getvalue().decode("utf-8")

    assert "BEGIN:VEVENT" in data
    assert "SUMMARY:🔥" in data
    assert "DTSTART" in data
    assert "DTEND" in data


def test_export_stream_all_day_event():
    exporter = ICSExporter()
    output = BytesIO()

    event = DummyEvent(
        emoji="🎉",
        start=datetime(2024, 1, 1),
        end=datetime(2024, 1, 2),
        is_all_day=True
    )

    exporter.export_stream(output, [event])
    data = output.getvalue().decode("utf-8")

    assert "SUMMARY:🎉" in data
    assert "DTSTART;VALUE=DATE" in data


def test_export_stream_empty_events():
    exporter = ICSExporter()
    output = BytesIO()

    with pytest.raises(ValidationError):
        exporter.export_stream(output, [])


def test_export_stream_missing_emoji():
    exporter = ICSExporter()
    output = BytesIO()

    event = DummyEvent(
        emoji=None,
        start=datetime(2024, 1, 1, 10, 0),
        end=datetime(2024, 1, 1, 11, 0)
    )

    with pytest.raises(AppException):
        exporter.export_stream(output, [event])


def test_export_stream_serialize_failure(monkeypatch):
    exporter = ICSExporter()
    output = BytesIO()

    event = DummyEvent(
        emoji="🔥",
        start=datetime(2024, 1, 1, 10, 0),
        end=datetime(2024, 1, 1, 11, 0)
    )

    def bad_serialize_iter():
        raise RuntimeError("boom")

    monkeypatch.setattr(
        "ics.Calendar.serialize_iter",
        lambda self: bad_serialize_iter()
    )

    with pytest.raises(AppException):
        exporter.export_stream(output, [event])
