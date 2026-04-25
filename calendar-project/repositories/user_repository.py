from models.database_models.user_model import UserModel
from db import db

class UserRepository:

    @staticmethod
    def get_all():
        return UserModel.query.all()

    @staticmethod
    def get_by_id(user_id):
        return UserModel.query.filter_by(id=user_id).first()

    @staticmethod
    def create(name, email):
        user = UserModel(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user, name, email):
        user.name = name
        user.email = email
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()