from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.schemas.mapping_schemas import (MappingSchema, MappingCreateSchema, MappingSetSchema, MappingSetCreateSchema)

from app.services.mappings_service import MappingService

mapping_bp = Blueprint("mapping", __name__)

mapping_schema = MappingSchema()
mapping_many_schema = MappingSchema(many=True)
set_schema = MappingSetSchema()
set_many_schema = MappingSetSchema(many=True)
set_create_schema = MappingSetCreateSchema()
mapping_create_schema = MappingCreateSchema()

@mapping_bp.route("/sets", methods=["GET"])
@jwt_required()
def get_sets():
    """
    Get all mapping sets for the logged-in user
    ---
    tags:
      - Mapping Sets
    security:
      - Bearer: []
    responses:
      200:
        description: List of mapping sets
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              mappings:
                type: array
                items:
                  type: object
                  properties:
                    id: {type: integer}
                    word: {type: string}
                    emoji: {type: string}
      403:
        description: Forbidden
      404:
        description: User not found
    """
    user_id = int(get_jwt_identity())

    sets = MappingService.get_user_sets(user_id)
    return set_many_schema.dump(sets), 200

@mapping_bp.route("/sets", methods=["POST"])
@jwt_required()
def create_set():
    """
    Create a new mapping set
    ---
    tags:
      - Mapping Sets
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name]
          properties:
            name: {type: string}
    responses:
      201:
        description: Mapping set created
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            mappings:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  word: {type: string}
                  emoji: {type: string}
      400:
        description: Validation Error
      404:
        description: User not found
    """
    user_id = int(get_jwt_identity())
    data = set_create_schema.load(request.get_json())

    mapping_set = MappingService.create_set(
        user_id,
        data["name"]
    )

    return set_schema.dump(mapping_set), 201


@mapping_bp.route("/sets/<int:set_id>", methods=["DELETE"])
@jwt_required()
def delete_set(set_id):
    """
    Delete a mapping set
    ---
    tags:
      - Mapping Sets
    security:
      - Bearer: []
    parameters:
      - name: set_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Deleted successfully
        schema:
          properties:
            message: {type: string}
      403:
        description: Forbidden
      404:
        description: Mapping set not found
    """
    user_id = int(get_jwt_identity())

    MappingService.delete_set(set_id, user_id)
    return {"message": "Deleted"}, 200

@mapping_bp.route("/sets/<int:set_id>", methods=["PUT"])
@jwt_required()
def update_set(set_id):
    """
    Update an entire mapping set
    ---
    tags:
      - Mapping Sets
    security:
      - Bearer: []
    parameters:
      - name: set_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, mappings]
          properties:
            name:
              type: string
            mappings:
              type: array
              items:
                type: object
                properties:
                  word: {type: string}
                  emoji: {type: string}
    responses:
      200:
        description: Updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            mappings:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  word: {type: string}
                  emoji: {type: string}
      400:
        description: Validation Error
      403:
        description: Forbidden
      404:
        description: Mapping set not found
    """
    user_id = int(get_jwt_identity())
    data = set_create_schema.load(request.get_json())

    updated = MappingService.update_set(
        set_id=set_id,
        user_id=user_id,
        name=data["name"],
        mappings=data["mappings"]
    )

    return set_schema.dump(updated), 200

@mapping_bp.route("/sets/<int:set_id>/mappings", methods=["GET"])
@jwt_required()
def get_mappings(set_id):
    """
    Get all mappings inside a mapping set
    ---
    tags:
      - Mappings
    security:
      - Bearer: []
    parameters:
      - name: set_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: List of mappings
        schema:
          type: array
          items:
            properties:
              id: {type: integer}
              word: {type: string}
              emoji: {type: string}
      403:
        description: Forbidden
      404:
        description: Mapping set not found
    """
    user_id = int(get_jwt_identity())

    mappings = MappingService.get_mappings(set_id, user_id)
    return mapping_many_schema.dump(mappings), 200

@mapping_bp.route("/sets/<int:set_id>/mappings", methods=["POST"])
@jwt_required()
def create_mapping(set_id):
    """
    Create a mapping (word → emoji) inside a set
    ---
    tags:
      - Mappings
    security:
      - Bearer: []
    parameters:
      - name: set_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [word, emoji]
          properties:
            word: {type: string}
            emoji: {type: string}
    responses:
      201:
        description: Mapping created
        schema:
          properties:
            id: {type: integer}
            word: {type: string}
            emoji: {type: string}
      400:
        description: Validation Error
      403:
        description: Forbidden
      404:
        description: Mapping set not found
    """
    user_id = int(get_jwt_identity())
    data = mapping_create_schema.load(request.get_json())

    mapping = MappingService.create_mapping(
        set_id,
        user_id,
        data["word"],
        data["emoji"]
    )

    return mapping_schema.dump(mapping), 201

@mapping_bp.route("/mappings/<int:mapping_id>", methods=["DELETE"])
@jwt_required()
def delete_mapping(mapping_id):
    """
    Delete a mapping
    ---
    tags:
      - Mappings
    security:
      - Bearer: []
    parameters:
      - name: mapping_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Mapping deleted
        schema:
          properties:
            message: {type: string}
      403:
        description: Not allowed
      404:
        description: Not found
    """
    user_id = int(get_jwt_identity())

    MappingService.delete_mapping(mapping_id, user_id)
    return {"message": "Deleted"}, 200