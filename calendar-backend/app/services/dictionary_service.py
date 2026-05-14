from app.repositories.dictionary_repository import DictionaryRepository
from app.repositories.user_repository import UserRepository
from app.exceptions import ForbiddenError, NotFoundError, ValidationError


class DictionaryService:

    @staticmethod
    def _assert_admin(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        if not user.is_admin:
            raise ForbiddenError("Admin privileges required")
    # -------------------
    # DICTIONARY METHODS
    # -------------------
    @staticmethod
    def get_all_dictionaries():
        return DictionaryRepository.get_all()

    @staticmethod
    def get_dictionary(dictionary_id):
        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise NotFoundError("Dictionary not found")

        return dictionary

    @staticmethod
    def create_dictionary(user_id, name, language, description=None):
        DictionaryService._assert_admin(user_id)

        if not name or not language:
            raise ValidationError("Name and language are required")

        return DictionaryRepository.create(name, language, description)

    @staticmethod
    def delete_dictionary(user_id, dictionary_id):
        DictionaryService._assert_admin(user_id)
        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise NotFoundError("Dictionary not found")

        DictionaryRepository.delete(dictionary)

    # -------------------
    # ENTRY METHODS
    # -------------------
    @staticmethod
    def get_entries(user_id, dictionary_id):
        DictionaryService._assert_admin(user_id)
        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise NotFoundError("Dictionary not found")

        return DictionaryRepository.get_entries(dictionary_id)

    @staticmethod
    def add_entry(user_id, dictionary_id, word, emoji):
        DictionaryService._assert_admin(user_id)

        if not word or not emoji:
            raise ValidationError("Word and emoji are required")

        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise NotFoundError("Dictionary not found")

        return DictionaryRepository.add_entry(dictionary_id, word, emoji)

    @staticmethod
    def delete_entry(user_id, dictionary_id, entry_id):
        DictionaryService._assert_admin(user_id)

        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise NotFoundError("Dictionary not found")

        entries = DictionaryRepository.get_entries(dictionary_id)
        entry = next((e for e in entries if e.id == entry_id), None)

        if not entry:
            raise NotFoundError("Entry not found")

        DictionaryRepository.delete_entry(entry)

    @staticmethod
    def bulk_insert_entries(user_id, dictionary_id, entries_dict):
        DictionaryService._assert_admin(user_id)

        if not isinstance(entries_dict, dict):
            raise ValidationError("Entries must be a dictionary")

        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise NotFoundError("Dictionary not found")

        if len(entries_dict) == 0:
            raise ValidationError("Entries cannot be empty")

        return DictionaryRepository.bulk_insert(dictionary_id, entries_dict)

    @staticmethod
    def to_dict(dictionary_id: int) -> dict:
        entries = DictionaryRepository.get_entries(dictionary_id)

        return {
            e.word.lower(): e.emoji
            for e in entries
        }