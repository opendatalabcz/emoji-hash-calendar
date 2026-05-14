from flask import Blueprint, request
from app.services.dictionary_service import DictionaryService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.schemas.dictionary_schemas import (DictionarySchema, DictionaryCreateSchema, DictionaryEntrySchema, DictionaryEntryCreateSchema)

dictionary_bp = Blueprint("dictionary", __name__)

dictionary_schema = DictionarySchema()
dictionary_many_schema = DictionarySchema(many=True)

entry_schema = DictionaryEntrySchema()
entry_many_schema = DictionaryEntrySchema(many=True)

dictionary_create_schema = DictionaryCreateSchema()
entry_create_schema = DictionaryEntryCreateSchema()

@dictionary_bp.route("/", methods=["GET"])
def get_all_dictionaries():
    """
    Get all dictionaries
    ---
    tags:
      - Dictionary
    responses:
      200:
        description: List of dictionaries
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              language:
                type: string
              description:
                type: string
              created_at:
                type: string
      403:
        description: Forbidden
    """
    dictionaries = DictionaryService.get_all_dictionaries()
    return dictionary_many_schema.dump(dictionaries), 200


@dictionary_bp.route("/<int:dictionary_id>", methods=["GET"])
def get_dictionary(dictionary_id):
    """
    Get a dictionary by ID
    ---
    tags:
      - Dictionary
    parameters:
      - name: dictionary_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Dictionary details
        schema:
          type: object
          properties:
            id: {type: integer}
            name: {type: string}
            language: {type: string}
            description: {type: string}
            created_at: {type: string}
      404:
        description: Dictionary not found
    """
    dictionary = DictionaryService.get_dictionary(dictionary_id)
    return dictionary_schema.dump(dictionary), 200

@dictionary_bp.route("/", methods=["POST"])
@jwt_required()
def create_dictionary():
    """
    Create a new dictionary
    Admins are able to create new dictionaries
    ---
    tags:
      - Dictionary
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, language]
          properties:
            name:
              type: string
            language:
              type: string
            description:
              type: string
    responses:
      201:
        description: Dictionary created
        schema:
          type: object
          properties:
            id: {type: integer}
            name: {type: string}
            language: {type: string}
            description: {type: string}
      400:
        description: Validation error
      403:
        description: Forbidden
    """
    user_id = int(get_jwt_identity())
    data = dictionary_create_schema.load(request.get_json())

    dictionary = DictionaryService.create_dictionary(
        user_id=user_id,
        name=data["name"],
        language=data["language"],
        description=data.get("description")
    )
    return dictionary_schema.dump(dictionary), 201

@dictionary_bp.route("/<int:dictionary_id>", methods=["DELETE"])
@jwt_required()
def delete_dictionary(dictionary_id):
    """
    Delete a dictionary
    Admins are able to delete a dictionary
    ---
    tags:
      - Dictionary
    security:
      - Bearer: []
    parameters:
      - name: dictionary_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Dictionary deleted
        schema:
          type: object
          properties:
            message:
              type: string
      403:
        description: Forbidden
      404:
        description: Dictionary not found
    """
    user_id = int(get_jwt_identity())

    DictionaryService.delete_dictionary(user_id, dictionary_id)
    return {"message": "Dictionary deleted"}, 200

# -------------------
# ENTRY ROUTES
# -------------------

@dictionary_bp.route("/<int:dictionary_id>/entries", methods=["GET"])
@jwt_required()
def get_entries(dictionary_id):
    """
    Get all entries in a dictionary
    Endpoint to view mappings inside dictionary
    ---
    tags:
      - Dictionary Entries
    security:
      - Bearer: []
    parameters:
      - name: dictionary_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: List of entries
        schema:
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
        description: Dictionary not found
    """
    user_id = int(get_jwt_identity())

    entries = DictionaryService.get_entries(user_id, dictionary_id)
    return entry_many_schema.dump(entries), 200

@dictionary_bp.route("/<int:dictionary_id>/entries", methods=["POST"])
@jwt_required()
def add_entry(dictionary_id):
    """
    Add a new entry to a dictionary
    ---
    tags:
      - Dictionary Entries
    security:
      - Bearer: []
    parameters:
      - name: dictionary_id
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
            word:
              type: string
            emoji:
              type: string
    responses:
      201:
        description: Entry created
        schema:
          type: object
          properties:
            id: {type: integer}
            word: {type: string}
            emoji: {type: string}
      400:
        description: Validation error
      403:
        description: Forbidden
      404:
        description: Dictionary not found
    """
    user_id = int(get_jwt_identity())
    data = entry_create_schema.load(request.get_json())

    entry = DictionaryService.add_entry(
        user_id=user_id,
        dictionary_id=dictionary_id,
        word=data["word"],
        emoji=data["emoji"]
    )
    return entry_schema.dump(entry), 201


@dictionary_bp.route("/<int:dictionary_id>/entries/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def delete_entry(dictionary_id, entry_id):
    """
    Delete an entry from a dictionary
    ---
    tags:
      - Dictionary Entries
    security:
      - Bearer: []
    parameters:
      - name: dictionary_id
        in: path
        type: integer
        required: true
      - name: entry_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Entry deleted
        schema:
          type: object
          properties:
            message:
              type: string
      403:
        description: Forbidden
      404:
        description: Entry not found
    """
    user_id = int(get_jwt_identity())

    DictionaryService.delete_entry(user_id, dictionary_id, entry_id)
    return {"message": "Entry deleted"}, 200

@dictionary_bp.route("/<int:dictionary_id>/entries/bulk", methods=["POST"])
@jwt_required()
def bulk_insert(dictionary_id):
    """
    Bulk insert entries into a dictionary
    Insert multiple mappings at once into dictionary, takes input in the form of JSON, where each row is "word":"emoji"
    ---
    tags:
      - Dictionary Entries
    security:
      - Bearer: []
    parameters:
      - name: dictionary_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          additionalProperties:
            type: string
          example:
            hello: "👋"
            world: "🌍"
    responses:
      201:
        description: Bulk insert successful
        schema:
          type: object
          properties:
            message: {type: string}
            inserted: {type: integer}
      400:
        description: Validation error
      403:
        description: Forbidden
      404:
        description: Dictionary not found
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    count = DictionaryService.bulk_insert_entries(
        user_id=user_id,
        dictionary_id=dictionary_id,
        entries_dict=data
    )
    return {"message": "Bulk insert successful", "inserted": count}, 201