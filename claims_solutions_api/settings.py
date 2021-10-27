import os
from datetime import timedelta

class Config(object):
    DEBUG = False
    TESTING = False

    SESSION_COOKIE_SECURE = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

    PROPOGATE_EXCEPTIONS = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'justin'
    JWT_SECRET_KEY = 'justin'

class TestingConfig(Config):
    TESTING = True
    