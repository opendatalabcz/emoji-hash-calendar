from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    #calendars = db.relationship("Calendar", backref="user", lazy=True)
    #mapping_sets = db.relationship("UserMappingSet", backref="user", lazy=True)
    #settings = db.relationship("Settings", backref="user", uselist=False)