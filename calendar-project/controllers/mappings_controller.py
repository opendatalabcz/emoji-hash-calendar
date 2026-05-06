from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.mappings_service import MappingService

mapping_bp = Blueprint("mapping", __name__)

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
                properties:
                  id:
                    type: integer
                  name:
                    type: string
    """
    user_id = int(get_jwt_identity())

    sets = MappingService.get_user_sets(user_id)

    return jsonify([
        {
            "id": s.id,
            "name": s.name
        }
        for s in sets
    ]), 200

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
              required:
                - name
              properties:
                name:
                  type: string
        responses:
          201:
            description: Mapping set created
            schema:
              properties:
                id:
                  type: integer
                name:
                  type: string
          400:
            description: Invalid input
        """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    try:
        mapping_set = MappingService.create_set(
            user_id,
            data.get("name")
        )

        return {
            "id": mapping_set.id,
            "name": mapping_set.name
        }, 201

    except ValueError as e:
        return {"error": str(e)}, 400


@mapping_bp.route("/sets/<int:set_id>", methods=["DELETE"])
@jwt_required()
def delete_set(set_id):
    """
        Delete a mapping set (only if owned by user)
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
          403:
            description: Not allowed
          404:
            description: Not found
        """
    user_id = int(get_jwt_identity())

    try:
        MappingService.delete_set(set_id, user_id)
        return {"message": "Deleted"}, 200

    except (ValueError, PermissionError) as e:
        return {"error": str(e)}, 403 if isinstance(e, PermissionError) else 404

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
                  id:
                    type: integer
                  word:
                    type: string
                  emoji:
                    type: string
          403:
            description: Not allowed
          404:
            description: Not found
        """
    user_id = int(get_jwt_identity())

    try:
        mappings = MappingService.get_mappings(set_id, user_id)

        return jsonify([
            {
                "id": m.id,
                "word": m.word,
                "emoji": m.emoji
            }
            for m in mappings
        ]), 200

    except (ValueError, PermissionError) as e:
        return {"error": str(e)}, 403 if isinstance(e, PermissionError) else 404

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
              required:
                - word
                - emoji
              properties:
                word:
                  type: string
                emoji:
                  type: string
        responses:
          201:
            description: Mapping created
            schema:
              properties:
                id:
                  type: integer
                word:
                  type: string
                emoji:
                  type: string
          400:
            description: Invalid input
          403:
            description: Not allowed
        """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    try:
        mapping = MappingService.create_mapping(
            set_id,
            user_id,
            data.get("word"),
            data.get("emoji")
        )

        return {
            "id": mapping.id,
            "word": mapping.word,
            "emoji": mapping.emoji
        }, 201

    except (ValueError, PermissionError) as e:
        return {"error": str(e)}, 400

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
            description: Deleted successfully
          403:
            description: Not allowed
          404:
            description: Not found
        """
    user_id = int(get_jwt_identity())

    try:
        MappingService.delete_mapping(mapping_id, user_id)
        return {"message": "Deleted"}, 200

    except (ValueError, PermissionError) as e:
        return {"error": str(e)}, 403 if isinstance(e, PermissionError) else 404

@mapping_bp.route("/sets/<int:set_id>", methods=["PUT"])
@jwt_required()
def update_set(set_id):
    """
    Update an entire mapping set (name + full mappings replace)
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
          required:
            - name
            - mappings
          properties:
            name:
              type: string
            mappings:
              type: array
              items:
                type: object
                properties:
                  word:
                    type: string
                  emoji:
                    type: string
    responses:
      200:
        description: Updated successfully
      400:
        description: Invalid input
      403:
        description: Not allowed
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()

    try:
        updated = MappingService.update_set(
            set_id=set_id,
            user_id=user_id,
            name=data.get("name"),
            mappings=data.get("mappings", [])
        )

        return {
            "id": updated.id,
            "name": updated.name
        }, 200

    except (ValueError, PermissionError) as e:
        return {"error": str(e)}, 403 if isinstance(e, PermissionError) else 400