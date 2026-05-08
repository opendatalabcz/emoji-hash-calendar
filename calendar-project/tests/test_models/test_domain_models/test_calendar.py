from app.models.domain_models.calendar import Calendar
from app.models.domain_models.event import Event


def test_add_event():
    calendar = Calendar()
    event = Event(title="Meeting", start="2026-05-08T10:00", end="2026-05-08T11:00")

    calendar.add_event(event)

    assert len(calendar) == 1
    assert calendar.get_events()[0] == event


def test_get_events_returns_list():
    calendar = Calendar()
    event1 = Event(title="Meeting", start="2026-05-08T10:00", end="2026-05-08T11:00")
    event2 = Event(title="Lunch", start="2026-05-08T12:00", end="2026-05-08T13:00")

    calendar.add_event(event1)
    calendar.add_event(event2)

    events = calendar.get_events()
    assert isinstance(events, list)
    assert len(events) == 2
    assert events[0].title == "Meeting"
    assert events[1].title == "Lunch"


def test_clear_events():
    calendar = Calendar()
    event = Event(title="Meeting", start="2026-05-08T10:00", end="2026-05-08T11:00")
    calendar.add_event(event)

    calendar.clear_events()

    assert len(calendar) == 0
    assert calendar.get_events() == []


def test_len_dunder_method():
    calendar = Calendar()
    for i in range(3):
        calendar.add_event(Event(title=f"Event {i}", start="2026-05-08T10:00", end="2026-05-08T11:00"))

    assert len(calendar) == 3
