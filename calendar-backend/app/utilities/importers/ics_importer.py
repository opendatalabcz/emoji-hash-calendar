from ics import Calendar as ICSCalendar
from app.models.domain_models.event import Event
from io import BytesIO
from app.exceptions import ValidationError


class ICSImporter:
    """Class for loading .ics data into internal Event objects."""

    def load_stream(self, input_stream: BytesIO):
        if not input_stream:
            raise ValidationError("Input ICS stream is empty")

        try:
            ics_str = input_stream.read().decode("utf-8")
        except Exception:
            raise ValidationError("ICS file is not valid UTF-8")

        return self._load_from_string(ics_str)

    @staticmethod
    def _load_from_string(ics_str: str):
        try:
            ics_cal = ICSCalendar(ics_str)
        except Exception as e:
            raise ValidationError(f"Failed to parse ICS file: {str(e)}")

        events = []

        for e in ics_cal.events:
            events.append(Event(
                title=e.name or "Untitled",
                start=e.begin,
                end=e.end,
                uid=getattr(e, "uid", None),
                status=getattr(e, "status", None),
                created=getattr(e, "created", None),
                last_modified=getattr(e, "last_modified", None),
                is_all_day=e.all_day,
                rrule=getattr(e, "rrule", None),
                rdate=getattr(e, "rdate", None),
                exdate=getattr(e, "exdate", None),
                recurrence_id=getattr(e, "recurrence_id", None),
                duration=getattr(e, "duration", None)
            ))

        if not events:
            raise ValidationError("ICS file contains no events")

        return events