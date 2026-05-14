from datetime import timedelta
from ics import Calendar as ICSCalendar, Event as ICSEvent
from io import BytesIO
from app.exceptions import ValidationError, AppException


class ICSExporter:
    """Export internal Event objects into an ICS file."""

    def export_stream(self, output_stream: BytesIO, events):
        if not events:
            raise ValidationError("Cannot export empty calendar")

        try:
            ics_cal = self._create_ics_calendar(events)
            ics_str = "".join(ics_cal.serialize_iter())
            output_stream.write(ics_str.encode("utf-8"))
            output_stream.seek(0)
        except Exception as e:
            raise AppException(f"Failed to export ICS: {str(e)}")

    @staticmethod
    def _create_ics_calendar(events):
        ics_cal = ICSCalendar()

        for e in events:
            if not e.emoji:
                raise ValidationError("Event is missing emoji title")

            new_event = ICSEvent(
                name=e.emoji,
                uid=e.uid,
                status=e.status
            )

            if e.created:
                new_event.created = e.created
            if e.last_modified:
                new_event.last_modified = e.last_modified

            if e.is_all_day:
                start_date = e.start.date()
                end_date = e.end.date()

                if end_date <= start_date:
                    end_date = start_date + timedelta(days=1)
                else:
                    end_date -= timedelta(days=1)

                new_event.begin = start_date
                new_event.end = end_date
                new_event.make_all_day()
            else:
                new_event.begin = e.start
                new_event.end = e.end

            if e.rrule:
                new_event.rrule = e.rrule

            if e.rdate:
                new_event.rdate = e.rdate

            if e.exdate:
                new_event.exdate = e.exdate

            if e.recurrence_id:
                new_event.recurrence_id = e.recurrence_id

            if e.duration:
                new_event.duration = e.duration
                
            ics_cal.events.add(new_event)

        return ics_cal
