from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.route("/", methods=["GET"])
def get_users():
    """
        Get all users
        ---
        tags:
          - Users
        responses:
          200:
            description: List of users
            schema:
              type: array
              items:
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
        """
    users = UserService.get_users()
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email}
        for u in users
    ])


@user_bp.route("/", methods=["POST"])
def create_user():
    """
        Create a new user
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - name
                - email
              properties:
                name:
                  type: string
                email:
                  type: string
        responses:
          201:
            description: User created successfully
            schema:
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
          400:
            description: Invalid input
        """
    data = request.get_json()
    try:
        user = UserService.create_user(data.get("name"), data.get("email"))
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }, 201
    except ValueError as e:
        return {"error": str(e)}, 400


@user_bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    """
        Get user by ID
        ---
        tags:
          - Users
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: User found
            schema:
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
          404:
            description: User not found
        """
    try:
        user = UserService.get_user(id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    except ValueError as e:
        return {"error": str(e)}, 404


@user_bp.route("/<int:id>", methods=["PATCH"])
def update_user(id):
    """
        Update user by ID
        ---
        tags:
          - Users
        parameters:
          - name: id
            in: path
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                email:
                  type: string
        responses:
          200:
            description: Updated user
            schema:
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
          404:
            description: User not found
        """
    data = request.get_json()
    try:
        user = UserService.update_user(id, data.get("name"), data.get("email"))
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    except ValueError as e:
        return {"error": str(e)}, 404


@user_bp.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    """
        Delete user by ID
        ---
        tags:
          - Users
        parameters:
          - name: id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: User deleted
            schema:
              properties:
                message:
                  type: string
          404:
            description: User not found
        """
    try:
        UserService.delete_user(id)
        return {"message": "Deleted"}
    except ValueError as e:
        return {"error": str(e)}, 404