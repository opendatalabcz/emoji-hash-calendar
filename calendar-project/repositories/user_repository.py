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
    def create(username, password):
        user = UserModel(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user, username, password):
        user.username = username
        user.password = password
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()