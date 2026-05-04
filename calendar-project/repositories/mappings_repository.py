from db import db
from models.database_models.mapping_model import Mapping
from models.database_models.user_mapping_model import UserMappingSet

class MappingRepository:

    # -------------------
    # MAPPING SETS
    # -------------------

    @staticmethod
    def get_all_sets_by_user(user_id):
        return UserMappingSet.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_set_by_id(set_id):
        return UserMappingSet.query.filter_by(id=set_id).first()

    @staticmethod
    def create_set(user_id, name):
        mapping_set = UserMappingSet(
            name=name,
            user_id=user_id
        )
        db.session.add(mapping_set)
        db.session.commit()
        return mapping_set

    @staticmethod
    def delete_set(mapping_set):
        db.session.delete(mapping_set)
        db.session.commit()

    # -------------------
    # MAPPINGS
    # -------------------

    @staticmethod
    def get_mappings_by_set(set_id):
        return Mapping.query.filter_by(mapping_set_id=set_id).all()

    @staticmethod
    def get_mapping_by_id(mapping_id):
        return Mapping.query.filter_by(id=mapping_id).first()

    @staticmethod
    def create_mapping(set_id, word, emoji):
        mapping = Mapping(
            word=word,
            emoji=emoji,
            mapping_set_id=set_id
        )
        db.session.add(mapping)
        db.session.commit()
        return mapping

    @staticmethod
    def delete_mapping(mapping):
        db.session.delete(mapping)
        db.session.commit()

    @staticmethod
    def delete_mappings_by_set(set_id):
        Mapping.query.filter_by(mapping_set_id=set_id).delete()
        db.session.commit()

    @staticmethod
    def save(obj):
        db.session.add(obj)
        db.session.commit()