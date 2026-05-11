from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv

from .extensions import db, jwt, migrate

from app.controllers.calendar_controller import calendar_bp
from app.controllers.user_controller import user_bp
from app.controllers.dictionary_controller import dictionary_bp
from app.controllers.mappings_controller import mapping_bp

from app.errors import register_error_handlers

def create_app(testing=False):
    load_dotenv()
    app = Flask(__name__)
    if testing:
        app.config.from_object("app.config.TestConfig")
    else:
        app.config.from_object("app.config.DevConfig")

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Calendar Transformer API",
            "version": "1.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: Bearer <your JWT token>"
            }
        },
        "definitions": {
            "UserModel": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "is_admin": {"type": "boolean"},
                    "mapping_sets": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/UserMappingSet"}
                    }
                }
            },

            "UserMappingSet": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "user_id": {"type": "integer"},
                    "mappings": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Mapping"}
                    }
                }
            },

            "Mapping": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "word": {"type": "string"},
                    "emoji": {"type": "string"},
                    "mapping_set_id": {"type": "integer"}
                }
            },

            "Dictionary": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "language": {"type": "string"},
                    "description": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "entries": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/DictionaryEntry"}
                    }
                }
            },

            "DictionaryEntry": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "word": {"type": "string"},
                    "emoji": {"type": "string"},
                    "dictionary_id": {"type": "integer"}
                }
            }
        }
    })

    app.register_blueprint(calendar_bp, url_prefix="/api/calendars")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(dictionary_bp, url_prefix="/api/dictionaries")
    app.register_blueprint(mapping_bp, url_prefix="/api/mappings")

    register_error_handlers(app)

    @app.route("/")
    def home():
        return "<h1>Welcome to Calendar Transformer!</h1>"

    return app