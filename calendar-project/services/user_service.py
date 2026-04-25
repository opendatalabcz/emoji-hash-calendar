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
    def create_user(name, email):
        if not name or not email:
            raise ValueError("Name and email required")
        return UserRepository.create(name, email)

    @staticmethod
    def update_user(user_id, name, email):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return UserRepository.update(user, name, email)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        UserRepository.delete(user)