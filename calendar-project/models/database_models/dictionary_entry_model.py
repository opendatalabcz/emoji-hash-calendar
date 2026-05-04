from db import db

class DictionaryEntry(db.Model):
    __tablename__ = "dictionary_entries"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), nullable=False)
    emoji = db.Column(db.String(5), nullable=False)

    dictionary_id = db.Column(db.Integer,db.ForeignKey("dictionaries.id", ondelete="CASCADE"),nullable=False)