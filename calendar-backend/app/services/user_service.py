from app.repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions import NotFoundError, ForbiddenError, ValidationError, AuthenticationError

class UserService:

    @staticmethod
    def assert_user_owns_resource(user_id, current_user_id):
        if user_id != current_user_id:
            raise ForbiddenError("Forbidden")

    @staticmethod
    def assert_admin(current_user):
        if not current_user.is_admin:
            raise ForbiddenError("Admin privileges required")

    @staticmethod
    def get_users():
        return UserRepository.get_all()

    @staticmethod
    def get_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    @staticmethod
    def create_user(username, password, confirm_password):

        if password != confirm_password:
            raise ValidationError("Passwords mismatch")

        existing = UserRepository.get_by_username(username)
        if existing:
            raise ValidationError("Username already taken")

        is_first_user = UserRepository.count() == 0

        hashed_password = generate_password_hash(password)
        return UserRepository.create(username, hashed_password, is_admin=is_first_user)

    @staticmethod
    def update_user_password(user_id, current_user_id, current_password, new_password, confirm_new_password):

        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        UserService.assert_user_owns_resource(user_id, current_user_id)

        if not check_password_hash(user.password, current_password):
            raise ValidationError("Incorrect password")

        if new_password != confirm_new_password:
            raise ValidationError("Passwords mismatch")

        hashed = generate_password_hash(new_password)
        return UserRepository.update_password(user, hashed)

    @staticmethod
    def make_admin(target_user_id, current_user_id):
        current_user = UserRepository.get_by_id(current_user_id)
        UserService.assert_admin(current_user)

        user = UserRepository.get_by_id(target_user_id)
        if not user:
            raise NotFoundError("User not found")
        if user.is_admin:
            return user

        return UserRepository.update_admin(user, True)

    @staticmethod
    def delete_user(user_id, current_user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        UserService.assert_user_owns_resource(user_id, current_user_id)

        UserRepository.delete(user)

    @staticmethod
    def authenticate(username, password):
        if not username or not password:
            raise AuthenticationError("Missing credentials")

        user = UserRepository.get_by_username(username)

        if not user:
            raise AuthenticationError("User not found")

        if not check_password_hash(user.password, password):
            raise AuthenticationError("Incorrect password")

        return user