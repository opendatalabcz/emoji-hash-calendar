from app.repositories.mappings_repository import MappingRepository
from app.exceptions import NotFoundError, ForbiddenError, ValidationError
from app.repositories.user_repository import UserRepository

class MappingService:

    @staticmethod
    def _assert_user_exists(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

    @staticmethod
    def _get_user_set(set_id, user_id):
        mapping_set = MappingRepository.get_set_by_id(set_id)

        if not mapping_set:
            raise NotFoundError("Mapping set not found")

        if mapping_set.user_id != user_id:
            raise ForbiddenError("Not allowed to access this mapping set")

        return mapping_set

    # -------------------
    # MAPPING SETS
    # -------------------

    @staticmethod
    def get_user_sets(user_id):
        MappingService._assert_user_exists(user_id)
        return MappingRepository.get_all_sets_by_user(user_id)

    @staticmethod
    def create_set(user_id, name):
        MappingService._assert_user_exists(user_id)
        if not name:
            raise ValidationError("Name is required")
        return MappingRepository.create_set(user_id, name)

    @staticmethod
    def delete_set(set_id, user_id):
        mapping_set = MappingService._get_user_set(set_id, user_id)
        MappingRepository.delete_set(mapping_set)

    # -------------------
    # MAPPINGS
    # -------------------

    @staticmethod
    def get_mappings(set_id, user_id):
        MappingService._get_user_set(set_id, user_id)

        return MappingRepository.get_mappings_by_set(set_id)

    @staticmethod
    def create_mapping(set_id, user_id, word, emoji):
        MappingService._get_user_set(set_id, user_id)

        if not word or not word.strip():
            raise ValidationError("Word is required")

        if not emoji:
            raise ValidationError("Emoji is required")

        return MappingRepository.create_mapping(set_id, word, emoji)

    @staticmethod
    def delete_mapping(mapping_id, user_id):
        mapping = MappingRepository.get_mapping_by_id(mapping_id)

        if not mapping:
            raise NotFoundError("Mapping not found")

        mapping_set = mapping.mapping_set

        if mapping_set.user_id != user_id:
            raise ForbiddenError("Not allowed to delete this mapping")

        MappingRepository.delete_mapping(mapping)

    @staticmethod
    def update_set(set_id, user_id, name, mappings):
        mapping_set = MappingService._get_user_set(set_id, user_id)

        if name:
            mapping_set.name = name.strip()

        MappingRepository.delete_mappings_by_set(set_id)

        for m in mappings:
            word = (m.get("word") or "").strip()
            emoji = m.get("emoji")

            if not word or not emoji:
                raise ValidationError("Each mapping must contain word and emoji")

            MappingRepository.create_mapping(set_id, word, emoji)

        MappingRepository.save(mapping_set)
        return mapping_set