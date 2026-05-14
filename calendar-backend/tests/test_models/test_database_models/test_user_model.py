from app.extensions import db
from app.models.database_models.user_model import UserModel

def test_create_user(app):
    with app.app_context():
        user = UserModel(
            username="duy",
            password="hashed-password",
            is_admin=False
        )

        db.session.add(user)
        db.session.commit()

        found = UserModel.query.filter_by(username="duy").first()

        assert found is not None
        assert found.username == "duy"
        assert found.password == "hashed-password"
        assert found.is_admin is False


def test_username_must_be_unique(app):
    with app.app_context():
        user1 = UserModel(username="duy", password="pw1")
        user2 = UserModel(username="duy", password="pw2")

        db.session.add(user1)
        db.session.commit()

        db.session.add(user2)

        from sqlalchemy.exc import IntegrityError

        try:
            db.session.commit()
            assert False, "Expected IntegrityError for duplicate username"
        except IntegrityError:
            db.session.rollback()


def test_default_is_admin_false(app):
    with app.app_context():
        user = UserModel(username="john", password="pw123")
        db.session.add(user)
        db.session.commit()

        found = UserModel.query.filter_by(username="john").first()
        assert found.is_admin is False


def test_user_relationship_mapping_sets(app):
    from app.models.database_models.user_mapping_model import UserMappingSet

    with app.app_context():
        user = UserModel(username="duy", password="pw")
        db.session.add(user)
        db.session.commit()

        mapping_set = UserMappingSet(name="My Set", user_id=user.id)
        db.session.add(mapping_set)
        db.session.commit()

        assert len(user.mapping_sets) == 1
        assert user.mapping_sets[0].name == "My Set"
