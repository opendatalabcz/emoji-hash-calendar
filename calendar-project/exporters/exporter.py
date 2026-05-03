from datetime import timedelta
from ics import Calendar as ICSCalendar, Event as ICSEvent
from io import BytesIO

class CalendarExporter:
    """Class for exporting events into an .ics file."""

    def export(self, filepath: str, events):
        ics_cal = self._create_ics_calendar(events)
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(ics_cal.serialize_iter())

    def export_stream(self, output_stream: BytesIO, events):
        """
        Write ICS calendar to an in-memory BytesIO stream.
        """
        ics_cal = self.create_ics_calendar(events)
        ics_str = "".join(ics_cal.serialize_iter())
        output_stream.write(ics_str.encode("utf-8"))
        output_stream.seek(0)

    def create_ics_calendar(self, events):
        ics_cal = ICSCalendar()

        for e in events:
            event_name = e.emoji
            new_event = ICSEvent(
                name=event_name,
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

            ics_cal.events.add(new_event)
        return ics_cal