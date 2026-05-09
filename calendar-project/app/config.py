import os

class Config:
    JWT_SECRET_KEY = "super-secret"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///calendar_transformer.db"
    #SQLALCHEMY_DATABASE_URI = "postgresql://postgres:example@db:5432/calendar_db"

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"