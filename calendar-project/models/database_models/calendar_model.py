from db import db
from datetime import datetime, timezone

class CalendarModel(db.Model):
    __tablename__ = "calendars"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)