import pytest
from io import BytesIO
from arrow import Arrow
from app.utilities.importers.ics_importer import ICSImporter
from app.exceptions import ValidationError


VALID_ICS = b"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Test Corp//Test Calendar//EN
BEGIN:VEVENT
UID:1
SUMMARY:Test Event
DTSTART:20240101T100000Z
DTEND:20240101T110000Z
END:VEVENT
END:VCALENDAR
"""

NO_EVENTS_ICS = b"""BEGIN:VCALENDAR
VERSION:2.0
END:VCALENDAR
"""

INVALID_ICS = b"NOT A VALID ICS FILE"


def test_load_stream_success():
    importer = ICSImporter()
    stream = BytesIO(VALID_ICS)

    events = importer.load_stream(stream)

    assert len(events) == 1
    assert events[0].title == "Test Event"
    assert isinstance(events[0].start, Arrow)
    assert isinstance(events[0].end, Arrow)


def test_load_stream_empty_stream():
    importer = ICSImporter()

    with pytest.raises(ValidationError):
        importer.load_stream(None)


def test_load_stream_invalid_utf8():
    importer = ICSImporter()
    stream = BytesIO(b"\xff\xfe\xfa\xfb")

    with pytest.raises(ValidationError):
        importer.load_stream(stream)


def test_load_stream_no_events():
    importer = ICSImporter()
    stream = BytesIO(NO_EVENTS_ICS)

    with pytest.raises(ValidationError):
        importer.load_stream(stream)


def test_load_stream_invalid_ics():
    importer = ICSImporter()
    stream = BytesIO(INVALID_ICS)

    with pytest.raises(ValidationError):
        importer.load_stream(stream)
