import os
from datetime import timedelta

class Config(object):
    DEBUG = False
    TESTING = False

    SESSION_COOKIE_SECURE = True

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    #
    # The "IMAGES" part of the following name must be the same name as the first
    # argument to "UploadSet" in "image_helper"
    #
    UPLOADED_IMAGES_DEST = os.path.join('claims_solutions_api', 'static', 'images')

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
    DEBUG = True

    PROPOGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'justin'
    JWT_SECRET_KEY = 'justin'