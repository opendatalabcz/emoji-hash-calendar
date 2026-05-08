import pytest
from app.extensions import db
from app.models.database_models.user_model import UserModel
from app.models.database_models.user_mapping_model import UserMappingSet
from app.models.database_models.mapping_model import Mapping


def test_create_user_mapping_set(app):
    """
    Ensure a UserMappingSet can be created and linked to a user.
    """
    with app.app_context():
        user = UserModel(username="duy", password="pw")
        db.session.add(user)
        db.session.commit()

        mapping_set = UserMappingSet(name="My Set", user_id=user.id)
        db.session.add(mapping_set)
        db.session.commit()

        found = UserMappingSet.query.filter_by(name="My Set").first()

        assert found is not None
        assert found.name == "My Set"
        assert found.user_id == user.id
        assert found.user.username == "duy"


def test_user_mapping_set_requires_user_id(app):
    """
    Ensure user_id is required (nullable=False).
    """
    with app.app_context():
        mapping_set = UserMappingSet(name="Invalid Set", user_id=None)
        db.session.add(mapping_set)

        from sqlalchemy.exc import IntegrityError

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()


def test_user_mapping_set_relationship_mappings(app):
    """
    Ensure the relationship to Mapping works.
    """
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

        assert len(mapping_set.mappings) == 1
        assert mapping_set.mappings[0].word == "hello"
        assert mapping_set.mappings[0].emoji == "👋"


def test_cascade_delete_orphan(app):
    """
    Ensure deleting a UserMappingSet also deletes its mappings.
    """
    with app.app_context():
        user = UserModel(username="duy", password="pw")
        db.session.add(user)
        db.session.commit()

        mapping_set = UserMappingSet(name="Cascade Set", user_id=user.id)
        db.session.add(mapping_set)
        db.session.commit()

        mapping = Mapping(word="bye", emoji="👋", mapping_set_id=mapping_set.id)
        db.session.add(mapping)
        db.session.commit()

        db.session.delete(mapping_set)
        db.session.commit()

        assert Mapping.query.count() == 0
