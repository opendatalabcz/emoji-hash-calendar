class Event:
    def __init__(
        self,
        title,
        start,
        end,
        uid=None,
        status=None,
        created=None,
        last_modified=None,
        is_all_day=False,
        rrule = None,
        rdate = None,
        exdate = None,
        recurrence_id = None,
        duration = None
    ):
        self.title = title
        self.start = start
        self.end = end
        self.uid = uid
        self.status = status
        self.created = created
        self.last_modified = last_modified
        self.is_all_day = is_all_day
        self.rrule = rrule
        self.rdate = rdate
        self.exdate = exdate
        self.recurrence_id = recurrence_id
        self.duration = duration
        self.emoji = None