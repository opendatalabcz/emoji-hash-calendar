import pytest
from app.extensions import db
from app.models.database_models.dictionary_model import Dictionary
from app.models.database_models.dictionary_entry_model import DictionaryEntry


def test_create_dictionary_entry(app):
    with app.app_context():
        dictionary = Dictionary(name="EmojiDict", language="en")
        db.session.add(dictionary)
        db.session.commit()

        entry = DictionaryEntry(
            word="hello",
            emoji="👋",
            dictionary_id=dictionary.id
        )
        db.session.add(entry)
        db.session.commit()

        found = DictionaryEntry.query.filter_by(word="hello").first()

        assert found is not None
        assert found.word == "hello"
        assert found.emoji == "👋"
        assert found.dictionary_id == dictionary.id
        assert found.dictionary.name == "EmojiDict"


def test_dictionary_entry_requires_word_and_emoji(app):
    with app.app_context():
        entry = DictionaryEntry(word=None, emoji=None, dictionary_id=1)
        db.session.add(entry)

        from sqlalchemy.exc import IntegrityError

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()


def test_dictionary_entry_requires_dictionary_id(app):
    with app.app_context():
        entry = DictionaryEntry(word="hello", emoji="👋", dictionary_id=None)
        db.session.add(entry)

        from sqlalchemy.exc import IntegrityError

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()


def test_dictionary_entry_backref(app):
    with app.app_context():
        dictionary = Dictionary(name="TestDict", language="en")
        db.session.add(dictionary)
        db.session.commit()

        entry = DictionaryEntry(
            word="bye",
            emoji="👋",
            dictionary_id=dictionary.id
        )
        db.session.add(entry)
        db.session.commit()

        assert entry.dictionary is not None
        assert entry.dictionary.name == "TestDict"
