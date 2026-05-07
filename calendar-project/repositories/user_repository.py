from models.database_models.user_model import UserModel
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.exceptions import ValidationError

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
            raise ValidationError("Username already taken")
        return user

    @staticmethod
    def update_password(user, password):
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