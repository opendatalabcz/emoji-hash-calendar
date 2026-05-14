from flask import Blueprint, request
from app.services.user_service import UserService
from app.models.schemas.user_schemas import UserCreateSchema, UserUpdateSchema, UserResponseSchema, LoginSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint("user", __name__)

create_schema = UserCreateSchema()
update_schema = UserUpdateSchema()
response_schema = UserResponseSchema()
response_many_schema = UserResponseSchema(many=True)
login_schema = LoginSchema()

@user_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    security:
      - Bearer: []
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            properties:
              id: {type: integer}
              username: {type: string}
              is_admin: {type: boolean}
      403:
        description: Forbidden
        """
    current_user_id = int(get_jwt_identity())
    current_user = UserService.get_user(current_user_id)
    UserService.assert_admin(current_user)

    users = UserService.get_users()
    return response_many_schema.dump(users), 200

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
          required: [username, password, confirm_password]
          properties:
            username: {type: string}
            password: {type: string}
            confirm_password: {type: string}
    responses:
      201:
        description: User created successfully
        schema:
          properties:
            id: {type: integer}
            username: {type: string}
            is_admin: {type: boolean}
            access_token: {type: string}
      400:
        description: Validation error
    """
    data = create_schema.load(request.get_json())

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

@user_bp.route("/<int:id>/admin", methods=["PUT"])
@jwt_required()
def set_admin(id):
    """
    Grant admin role to a user
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
        description: Admin role granted
        schema:
          type: object
          items:
            properties:
              id: {type: integer}
              username: {type: string}
              is_admin: {type: boolean}
      403:
        description: Forbidden
      404:
        description: User not found
    """
    current_user_id = int(get_jwt_identity())

    user = UserService.make_admin(id, current_user_id)

    return response_schema.dump(user), 200

@user_bp.route("/<int:id>/password", methods=["PUT"])
@jwt_required()
def update_user_password(id):
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
            current_password: {type: string}
            new_password: {type: string}
            confirm_new_password: {type: string}
    responses:
      200:
        description: Updated user
        schema:
          properties:
            id: {type: integer}
            username: {type: string}
            is_admin: {type: boolean}
      403:
        description: Forbidden
      400:
        description: Validation error
    """
    data = update_schema.load(request.get_json())
    current_user_id = int(get_jwt_identity())

    user = UserService.update_user_password(
        id,
        current_user_id,
        data["current_password"],
        data["new_password"],
        data["confirm_new_password"]
    )

    return response_schema.dump(user), 200



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
            message: {type: string}
      403:
        description: Forbidden
      404:
        description: User not found
    """
    current_user_id = int(get_jwt_identity())

    UserService.delete_user(id, current_user_id)
    return {"message": "Deleted"}, 200

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
          required: [username, password]
          properties:
            username: {type: string}
            password: {type: string}
    responses:
      200:
        description: Login successful
        schema:
          properties:
            access_token: {type: string}
      401:
        description: Authentication failed
    """
    data = login_schema.load(request.get_json())

    user = UserService.authenticate(
        data.get("username"),
        data.get("password")
    )

    token = create_access_token(identity=str(user.id))

    return {"access_token": token}, 200

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
            id: {type: integer}
            username: {type: string}
            is_admin: {type: boolean}
      404:
        description: User not found
    """
    user_id = int(get_jwt_identity())
    user = UserService.get_user(user_id)

    return response_schema.dump(user), 200