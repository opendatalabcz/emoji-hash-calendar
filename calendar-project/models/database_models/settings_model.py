from db import db

class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
