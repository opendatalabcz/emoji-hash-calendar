from db import db

class Mapping(db.Model):
    __tablename__ = "mappings"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(80), nullable=False)
    emoji = db.Column(db.String(5), nullable=False)

    mapping_set_id = db.Column(db.Integer, db.ForeignKey("user_mapping_sets.id"), nullable=False)