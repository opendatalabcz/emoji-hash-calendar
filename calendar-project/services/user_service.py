from repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:

    @staticmethod
    def get_users():
        return UserRepository.get_all()

    @staticmethod
    def get_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    def create_user(username, password):
        if not username or not password:
            raise ValueError("Username and password required")

        hashed_password = generate_password_hash(password)
        return UserRepository.create(username, hashed_password)

    @staticmethod
    def update_user(user_id, username, password):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        hashed_password = generate_password_hash(password)
        return UserRepository.update(user, username, hashed_password)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        UserRepository.delete(user)

    @staticmethod
    def authenticate(username, password):
        user = UserRepository.get_by_username(username)

        if not user:
            return None

        if not check_password_hash(user.password, password):
            return None

        return user