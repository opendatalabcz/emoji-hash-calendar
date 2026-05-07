class AppException(Exception):
    """Base application exception"""
    status_code = 400

    def __init__(self, message):
        self.message = message
        super().__init__(message)

class NotFoundError(AppException):
    status_code = 404

class ValidationError(AppException):
    status_code = 400

class AuthenticationError(AppException):
    status_code = 401

class ForbiddenError(AppException):
    status_code = 403