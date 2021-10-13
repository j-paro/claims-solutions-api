import os

class Config(object):
    DEBUG = False
    TESTING = False

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'justin'
    JWT_SECRET_KEY = 'justin'

class TestingConfig(Config):
    TESTING = True
    