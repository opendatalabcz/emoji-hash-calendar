from app.extensions import db
from datetime import datetime, timezone

class Dictionary(db.Model):
    __tablename__ = "dictionaries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    entries = db.relationship("DictionaryEntry", backref="dictionary", lazy=True, cascade="all, delete-orphan")