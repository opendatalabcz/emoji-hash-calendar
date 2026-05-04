from flask import Blueprint, request, jsonify
from services.dictionary_service import DictionaryService

from flasgger import swag_from

dictionary_bp = Blueprint("dictionary", __name__)

# -------------------
# DICTIONARY ROUTES
# -------------------

@dictionary_bp.route("/", methods=["GET"])
@swag_from({
    "tags": ["Dictionary"],
    "responses": {
        200: {
            "description": "List all dictionaries",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "language": {"type": "string"},
                        "description": {"type": "string"},
                        "created_at": {"type": "string"}
                    }
                }
            }
        }
    }
})
def get_all_dictionaries():
    dictionaries = DictionaryService.get_all_dictionaries()

    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "language": d.language,
            "description": d.description,
            "created_at": d.created_at.isoformat()
        }
        for d in dictionaries
    ]), 200


@dictionary_bp.route("/<int:dictionary_id>", methods=["GET"])
@swag_from({
    "tags": ["Dictionary"],
    "parameters": [
        {
            "name": "dictionary_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        200: {"description": "Dictionary found"},
        404: {"description": "Dictionary not found"}
    }
})
def get_dictionary(dictionary_id):
    try:
        dictionary = DictionaryService.get_dictionary(dictionary_id)

        return jsonify({
            "id": dictionary.id,
            "name": dictionary.name,
            "language": dictionary.language,
            "description": dictionary.description,
            "created_at": dictionary.created_at.isoformat()
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@dictionary_bp.route("/", methods=["POST"])
@swag_from({
    "tags": ["Dictionary"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["name", "language"],
                "properties": {
                    "name": {"type": "string"},
                    "language": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Dictionary created"},
        400: {"description": "Invalid input"}
    }
})
def create_dictionary():
    data = request.get_json()

    try:
        dictionary = DictionaryService.create_dictionary(
            name=data.get("name"),
            language=data.get("language"),
            description=data.get("description")
        )

        return jsonify({
            "id": dictionary.id,
            "name": dictionary.name,
            "language": dictionary.language,
            "description": dictionary.description
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@dictionary_bp.route("/<int:dictionary_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Dictionary"],
    "parameters": [
        {
            "name": "dictionary_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        200: {"description": "Deleted successfully"},
        404: {"description": "Dictionary not found"}
    }
})
def delete_dictionary(dictionary_id):
    try:
        DictionaryService.delete_dictionary(dictionary_id)
        return jsonify({"message": "Dictionary deleted"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# -------------------
# ENTRY ROUTES
# -------------------

@dictionary_bp.route("/<int:dictionary_id>/entries", methods=["GET"])
@swag_from({
    "tags": ["Dictionary Entries"],
    "parameters": [
        {
            "name": "dictionary_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        200: {"description": "List entries"},
        404: {"description": "Dictionary not found"}
    }
})
def get_entries(dictionary_id):
    try:
        entries = DictionaryService.get_entries(dictionary_id)

        return jsonify([
            {
                "id": e.id,
                "word": e.word,
                "emoji": e.emoji
            }
            for e in entries
        ]), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@dictionary_bp.route("/<int:dictionary_id>/entries", methods=["POST"])
@swag_from({
    "tags": ["Dictionary Entries"],
    "parameters": [
        {"name": "dictionary_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["word", "emoji"],
                "properties": {
                    "word": {"type": "string"},
                    "emoji": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Entry created"},
        400: {"description": "Invalid input"}
    }
})
def add_entry(dictionary_id):
    data = request.get_json()

    try:
        entry = DictionaryService.add_entry(
            dictionary_id=dictionary_id,
            word=data.get("word"),
            emoji=data.get("emoji")
        )

        return jsonify({
            "id": entry.id,
            "word": entry.word,
            "emoji": entry.emoji
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@dictionary_bp.route("/<int:dictionary_id>/entries/<int:entry_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Dictionary Entries"],
    "parameters": [
        {"name": "dictionary_id", "in": "path", "type": "integer", "required": True},
        {"name": "entry_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        200: {"description": "Deleted successfully"},
        404: {"description": "Entry not found"}
    }
})
def delete_entry(dictionary_id, entry_id):
    try:
        DictionaryService.delete_entry(dictionary_id, entry_id)
        return jsonify({"message": "Entry deleted"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


# -------------------
# BULK INSERT ROUTE
# -------------------

@dictionary_bp.route("/<int:dictionary_id>/entries/bulk", methods=["POST"])
@swag_from({
    "tags": ["Dictionary Entries"],
    "parameters": [
        {"name": "dictionary_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "additionalProperties": {
                    "type": "string"
                },
                "example": {
                    "christmas": "🎄",
                    "new year": "🎆"
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Bulk insert successful"},
        400: {"description": "Invalid payload"}
    }
})
def bulk_insert(dictionary_id):
    data = request.get_json()

    try:
        count = DictionaryService.bulk_insert_entries(
            dictionary_id=dictionary_id,
            entries_dict=data
        )

        return jsonify({
            "message": "Bulk insert successful",
            "inserted": count
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
