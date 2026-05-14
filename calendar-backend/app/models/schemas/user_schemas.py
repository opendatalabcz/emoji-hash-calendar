from marshmallow import Schema, fields, validate, pre_load

username_regex = r"^[a-z0-9_]+$"
password_regex = r"^(?=.*\d)(?=.*[A-Z])(?=.*[a-z]).{8,}$"

class UserCreateSchema(Schema):
    @pre_load
    def normalize(self, data, **kwargs):
        if not data:
            return data

        if "username" in data and data["username"]:
            data["username"] = data["username"].strip().lower()

        if "password" in data and isinstance(data["password"], str):
            data["password"] = data["password"].strip()

        if "confirm_password" in data and isinstance(data["confirm_password"], str):
            data["confirm_password"] = data["confirm_password"].strip()

        return data

    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=20),
            validate.Regexp(
                username_regex,
                error="Username can only contain letters, numbers, and underscores"
            )
        ]
    )
    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8),
            validate.Regexp(
                password_regex,
                error="Password must be at least 8 characters and contain a number, a capital letter and a small letter")
        ]
    )
    confirm_password = fields.String(required=True)

class UserUpdateSchema(Schema):
    @pre_load
    def normalize(self, data, **kwargs):
        if not data:
            return data

        for field in ["current_password", "new_password", "confirm_new_password"]:
            if field in data and isinstance(data[field], str):
                data[field] = data[field].strip()

        return data

    current_password = fields.String(required=True)
    new_password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8),
            validate.Regexp(password_regex, error="Password must be at least 8 characters and contain a number, a capital letter and a small letter")
        ]
    )
    confirm_new_password = fields.String(required=True)

class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.String()
    is_admin = fields.Boolean()

class LoginSchema(Schema):
    @pre_load
    def normalize(self, data, **kwargs):
        if not data:
            return data

        if "username" in data and isinstance(data["username"], str):
            data["username"] = data["username"].strip().lower()

        if "password" in data and isinstance(data["password"], str):
            data["password"] = data["password"].strip()

        return data

    username = fields.String(required=True)
    password = fields.String(required=True)