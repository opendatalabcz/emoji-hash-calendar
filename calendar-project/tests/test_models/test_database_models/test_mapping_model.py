import pytest
from app.extensions import db
from app.models.database_models.mapping_model import Mapping
from app.models.database_models.user_model import UserModel
from app.models.database_models.user_mapping_model import UserMappingSet


def test_create_mapping(app):
    with app.app_context():
        user = UserModel(username="duy", password="pw")
        db.session.add(user)
        db.session.commit()

        mapping_set = UserMappingSet(name="Emoji Set", user_id=user.id)
        db.session.add(mapping_set)
        db.session.commit()

        mapping = Mapping(word="hello", emoji="👋", mapping_set_id=mapping_set.id)
        db.session.add(mapping)
        db.session.commit()

        found = Mapping.query.filter_by(word="hello").first()

        assert found is not None
        assert found.word == "hello"
        assert found.emoji == "👋"
        assert found.mapping_set_id == mapping_set.id
        assert found.mapping_set.name == "Emoji Set"


def test_mapping_requires_word_and_emoji(app):
    with app.app_context():
        mapping = Mapping(word=None, emoji=None, mapping_set_id=1)
        db.session.add(mapping)

        from sqlalchemy.exc import IntegrityError

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()


def test_mapping_requires_mapping_set_id(app):
    with app.app_context():
        mapping = Mapping(word="hello", emoji="👋", mapping_set_id=None)
        db.session.add(mapping)

        from sqlalchemy.exc import IntegrityError

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()


def test_mapping_relationship_backref(app):
    with app.app_context():
        user = UserModel(username="john", password="pw")
        db.session.add(user)
        db.session.commit()

        mapping_set = UserMappingSet(name="Test Set", user_id=user.id)
        db.session.add(mapping_set)
        db.session.commit()

        mapping = Mapping(word="bye", emoji="👋", mapping_set_id=mapping_set.id)
        db.session.add(mapping)
        db.session.commit()

        assert mapping.mapping_set is not None
        assert mapping.mapping_set.name == "Test Set"
