import pytest
from app.extensions import db
from app.models.database_models.dictionary_model import Dictionary
from app.models.database_models.dictionary_entry_model import DictionaryEntry


def test_create_dictionary(app):
    """
    Ensure a Dictionary can be created and persisted.
    """
    with app.app_context():
        dictionary = Dictionary(
            name="Emoji Dictionary",
            language="en",
            description="Test dictionary"
        )

        db.session.add(dictionary)
        db.session.commit()

        found = Dictionary.query.filter_by(name="Emoji Dictionary").first()

        assert found is not None
        assert found.name == "Emoji Dictionary"
        assert found.language == "en"
        assert found.description == "Test dictionary"
        assert found.created_at is not None  # default timestamp works


def test_dictionary_name_must_be_unique(app):
    """
    name has unique=True, so duplicates must fail.
    """
    with app.app_context():
        d1 = Dictionary(name="MyDict", language="en")
        d2 = Dictionary(name="MyDict", language="en")

        db.session.add(d1)
        db.session.commit()

        db.session.add(d2)

        from sqlalchemy.exc import IntegrityError

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()


def test_dictionary_relationship_entries(app):
    """
    Relationship: Dictionary -> DictionaryEntry (one-to-many).
    """
    with app.app_context():
        dictionary = Dictionary(name="TestDict", language="en")
        db.session.add(dictionary)
        db.session.commit()

        entry = DictionaryEntry(
            word="hello",
            emoji="👋",
            dictionary_id=dictionary.id
        )

        db.session.add(entry)
        db.session.commit()

        assert len(dictionary.entries) == 1
        assert dictionary.entries[0].word == "hello"
        assert dictionary.entries[0].emoji == "👋"


def test_cascade_delete_entries(app):
    """
    Cascade rule: deleting a Dictionary should delete its entries.
    """
    with app.app_context():
        dictionary = Dictionary(name="CascadeDict", language="en")
        db.session.add(dictionary)
        db.session.commit()

        entry = DictionaryEntry(
            word="bye",
            emoji="👋",
            dictionary_id=dictionary.id
        )

        db.session.add(entry)
        db.session.commit()

        db.session.delete(dictionary)
        db.session.commit()

        assert DictionaryEntry.query.count() == 0
