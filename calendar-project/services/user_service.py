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
    def create_user(username, password, confirm_password):

        if password != confirm_password:
            raise ValueError("Passwords mismatch")

        existing = UserRepository.get_by_username(username)
        if existing:
            raise ValueError("Username already taken")

        hashed_password = generate_password_hash(password)
        return UserRepository.create(username, hashed_password)

    @staticmethod
    def update_user(user_id, current_password, new_password, confirm_new_password):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if not check_password_hash(user.password, current_password):
            raise ValueError("Incorrect password")

        if new_password != confirm_new_password:
            raise ValueError("Passwords mismatch")

        hashed = generate_password_hash(new_password)
        return UserRepository.update(user, hashed)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        UserRepository.delete(user)

    @staticmethod
    def authenticate(username, password):
        username = username.strip().lower() if username else None
        password = password.strip() if password else None

        if not username or not password:
            return None

        user = UserRepository.get_by_username(username)

        if not user:
            return None

        if not check_password_hash(user.password, password):
            return None

        return user