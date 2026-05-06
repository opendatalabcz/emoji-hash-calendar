from models.database_models.user_model import UserModel
from db import db
from sqlalchemy.exc import IntegrityError

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
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Username already taken")
        return user

    @staticmethod
    def update(user, password):
        user.password = password
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def get_by_username(username):
        return UserModel.query.filter_by(username=username).first()