from app.models.database_models.dictionary_model import Dictionary
from app.models.database_models.dictionary_entry_model import DictionaryEntry
from app.extensions import db


class DictionaryRepository:

    # -------------------
    # DICTIONARY METHODS
    # -------------------
    @staticmethod
    def get_all():
        return Dictionary.query.all()

    @staticmethod
    def get_by_id(dictionary_id):
        return Dictionary.query.filter_by(id=dictionary_id).first()

    @staticmethod
    def create(name, language, description=None):
        dictionary = Dictionary(
            name=name,
            language=language,
            description=description
        )
        db.session.add(dictionary)
        db.session.commit()
        return dictionary

    @staticmethod
    def delete(dictionary):
        db.session.delete(dictionary)
        db.session.commit()

    # -------------------
    # ENTRY METHODS
    # -------------------
    @staticmethod
    def get_entries(dictionary_id):
        return DictionaryEntry.query.filter_by(dictionary_id=dictionary_id).all()

    @staticmethod
    def add_entry(dictionary_id, word, emoji):
        entry = DictionaryEntry(
            word=word,
            emoji=emoji,
            dictionary_id=dictionary_id
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def delete_entry(entry):
        db.session.delete(entry)
        db.session.commit()

    @staticmethod
    def bulk_insert(dictionary_id, entries_dict):
        rows = [
            {"word": word, "emoji": emoji, "dictionary_id": dictionary_id}
            for word, emoji in entries_dict.items()
        ]

        db.session.bulk_insert_mappings(DictionaryEntry, rows)
        db.session.commit()

        return len(rows)