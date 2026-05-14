from app.models.domain_models.event import Event


def test_event_initialization_minimal():
    event = Event(
        title="Meeting",
        start="2026-05-08T10:00",
        end="2026-05-08T11:00"
    )

    assert event.title == "Meeting"
    assert event.start == "2026-05-08T10:00"
    assert event.end == "2026-05-08T11:00"

    assert event.uid is None
    assert event.status is None
    assert event.created is None
    assert event.last_modified is None
    assert event.is_all_day is False
    assert event.emoji is None


def test_event_initialization_full():
    event = Event(
        title="Lunch",
        start="2026-05-08T12:00",
        end="2026-05-08T13:00",
        uid="12345",
        status="CONFIRMED",
        created="2026-05-01T09:00",
        last_modified="2026-05-02T10:00",
        is_all_day=True
    )

    assert event.uid == "12345"
    assert event.status == "CONFIRMED"
    assert event.created == "2026-05-01T09:00"
    assert event.last_modified == "2026-05-02T10:00"
    assert event.is_all_day is True


def test_event_emoji_assignment():
    event = Event(
        title="Workout",
        start="2026-05-08T07:00",
        end="2026-05-08T08:00"
    )

    event.emoji = "💪"
    assert event.emoji == "💪"
