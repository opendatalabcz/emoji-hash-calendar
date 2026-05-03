from db import db

class UserMappingSet(db.Model):
    __tablename__ = "user_mapping_sets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    mappings = db.relationship("Mapping", backref="mapping_set", lazy=True)