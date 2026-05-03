from repositories.user_repository import UserRepository

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
        return UserRepository.create(username, password)

    @staticmethod
    def update_user(user_id, username, password):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return UserRepository.update(user, username, password)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        UserRepository.delete(user)