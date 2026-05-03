from repositories.dictionary_repository import DictionaryRepository


class DictionaryService:

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
            raise ValueError("Dictionary not found")

        return dictionary

    @staticmethod
    def create_dictionary(name, language, description=None):
        if not name or not language:
            raise ValueError("Name and language are required")

        return DictionaryRepository.create(name, language, description)

    @staticmethod
    def delete_dictionary(dictionary_id):
        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise ValueError("Dictionary not found")

        DictionaryRepository.delete(dictionary)

    # -------------------
    # ENTRY METHODS
    # -------------------
    @staticmethod
    def get_entries(dictionary_id):
        # ensure dictionary exists
        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise ValueError("Dictionary not found")

        return DictionaryRepository.get_entries(dictionary_id)

    @staticmethod
    def add_entry(dictionary_id, word, emoji):
        if not word or not emoji:
            raise ValueError("Word and emoji are required")

        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise ValueError("Dictionary not found")

        return DictionaryRepository.add_entry(dictionary_id, word, emoji)

    @staticmethod
    def delete_entry(dictionary_id, entry_id):
        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise ValueError("Dictionary not found")

        entries = DictionaryRepository.get_entries(dictionary_id)
        entry = next((e for e in entries if e.id == entry_id), None)

        if not entry:
            raise ValueError("Entry not found")

        DictionaryRepository.delete_entry(entry)

    # -------------------
    # BULK INSERT (MAIN FEATURE)
    # -------------------
    @staticmethod
    def bulk_insert_entries(dictionary_id, entries_dict):
        if not isinstance(entries_dict, dict):
            raise ValueError("Entries must be a dictionary")

        dictionary = DictionaryRepository.get_by_id(dictionary_id)

        if not dictionary:
            raise ValueError("Dictionary not found")

        if len(entries_dict) == 0:
            raise ValueError("Entries cannot be empty")

        return DictionaryRepository.bulk_insert(dictionary_id, entries_dict)

    @staticmethod
    def to_dict(dictionary_id: int) -> dict:
        entries = DictionaryRepository.get_entries(dictionary_id)

        return {
            e.word.lower(): e.emoji
            for e in entries
        }