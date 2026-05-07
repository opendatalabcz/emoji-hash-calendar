from flask import jsonify
from marshmallow import ValidationError as MarshmallowValidationError
from app.exceptions import AppException


def register_error_handlers(app):

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow(err):
        return jsonify({
            "error": "Validation failed",
            "details": err.messages
        }), 400


    @app.errorhandler(AppException)
    def handle_app_exception(err):
        return jsonify({
            "error": {
                "type": err.__class__.__name__,
                "message": err.message
            }
        }), err.status_code


    @app.errorhandler(404)
    def not_found(err):
        return jsonify({
            "error": "Not found"
        }), 404


    @app.errorhandler(500)
    def server_error(err):
        return jsonify({
            "error": "Internal server error"
        }), 500