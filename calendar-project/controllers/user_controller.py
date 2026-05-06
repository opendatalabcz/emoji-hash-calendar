from flask import Blueprint, request, jsonify
from services.user_service import UserService
from models.schemas.user_schemas import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint("user", __name__)

create_schema = UserCreateSchema()
update_schema = UserUpdateSchema()
response_schema = UserResponseSchema()
response_many_schema = UserResponseSchema(many=True)

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
                  username:
                    type: string
        """
    users = UserService.get_users()
    return jsonify(response_many_schema.dump(users)), 200

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
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
                confirm_password:
                  type: string
        responses:
          201:
            description: User created successfully
            schema:
              properties:
                id:
                  type: integer
                username:
                  type: string
                access_token:
                  type: string
          400:
            description: Invalid input
        """
    data = create_schema.load(request.get_json())

    try:
        user = UserService.create_user(
            data["username"],
            data["password"],
            data["confirm_password"]
        )

        token = create_access_token(identity=str(user.id))

        return {
            **response_schema.dump(user),
            "access_token": token
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
                username:
                  type: string
          404:
            description: User not found
        """
    try:
        user = UserService.get_user(id)
        return response_schema.dump(user), 200
    except ValueError as e:
        return {"error": str(e)}, 404


@user_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    """
            Update user by ID
            ---
            tags:
              - Users
            security:
              - Bearer: []
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
                    current_password:
                      type: string
                    new_password:
                      type: string
                    confirm_new_password:
                      type: string
            responses:
              200:
                description: Updated user
                schema:
                  properties:
                    id:
                      type: integer
                    username:
                      type: string
              404:
                description: User not found
            """
    data = update_schema.load(request.get_json())

    current_user_id = int(get_jwt_identity())
    if current_user_id != id:
        return {"error": "Forbidden"}, 403

    try:
        user = UserService.update_user(
            id,
            data["current_password"],
            data["new_password"],
            data["confirm_new_password"]
        )

        return response_schema.dump(user), 200

    except ValueError as e:
        return {"error": str(e)}, 404


@user_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    """
        Delete user by ID
        ---
        tags:
          - Users
        security:
          - Bearer: []
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
    current_user_id = int(get_jwt_identity())

    if current_user_id != id:
        return {"error": "Forbidden"}, 403

    try:
        UserService.delete_user(id)
        return {"message": "Deleted"}, 200
    except ValueError as e:
        return {"error": str(e)}, 404

@user_bp.route("/login", methods=["POST"])
def login():
    """
    User login
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
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
        schema:
          properties:
            access_token:
              type: string
      401:
        description: Invalid credentials
    """
    data = request.get_json()

    if not data:
        return {"error": "Missing JSON body"}, 400

    user = UserService.authenticate(
        data.get("username"),
        data.get("password")
    )

    if not user:
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=str(user.id))

    return {
        "access_token": token
    }, 200

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """
        Get current authenticated user
        ---
        tags:
          - Users
        security:
          - Bearer: []
        responses:
          200:
            description: Current user information
            schema:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
          401:
            description: Missing or invalid JWT token
          404:
            description: User not found
        """
    user_id = int(get_jwt_identity())
    user = UserService.get_user(user_id)

    return response_schema.dump(user), 200