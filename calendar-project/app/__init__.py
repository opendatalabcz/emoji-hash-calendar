from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from .extensions import db, jwt

from app.controllers.calendar_controller import calendar_bp
from app.controllers.user_controller import user_bp
from app.controllers.dictionary_controller import dictionary_bp
from app.controllers.mappings_controller import mapping_bp

from app.errors import register_error_handlers

def create_app():

    app = Flask(__name__)

    # -------------------
    # Config
    # -------------------
    CORS(app)

    app.config["JWT_SECRET_KEY"] = "super-secret"  # move to env later
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///calendar_transformer.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:example@db:5432/calendar_db"

    # -------------------
    # Extensions init
    # -------------------
    db.init_app(app)
    jwt.init_app(app)

    Swagger(app, template={
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: Bearer <your JWT token>"
            }
        }
    })

    # -------------------
    # Blueprints
    # -------------------
    app.register_blueprint(calendar_bp, url_prefix="/api/calendars")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(dictionary_bp, url_prefix="/api/dictionaries")
    app.register_blueprint(mapping_bp, url_prefix="/api/mappings")

    # -------------------
    # Error handlers
    # -------------------
    register_error_handlers(app)

    # -------------------
    # DB init (dev only)
    # -------------------
    with app.app_context():
        db.create_all()

    # -------------------
    # Routes
    # -------------------
    @app.route("/")
    def home():
        return "<h1>Welcome to Calendar Transformer!</h1>"

    return app