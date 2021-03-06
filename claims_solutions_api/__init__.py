import logging
import os
import sys
from flask import Flask
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class

from claims_solutions_api.models import db
from claims_solutions_api.models.blacklisted_token import BlacklistedToken
from claims_solutions_api.resources import api
from claims_solutions_api.schemas import ma
from claims_solutions_api.security import jwt
from claims_solutions_api.settings import (
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig
)
from claims_solutions_api.libs.image_helper import IMAGE_SET
from claims_solutions_api.errors import (
    ExpiredTokenError,
    InvalidTokenError,
    MissingTokenError,
    StaleTokenError,
    RevokedTokenError
)

def create_app():
    app = Flask(__name__.split('.')[0])
    
    configure_app(app)
    register_extensions(app)
    configure_logger(app)
    return app


def configure_app(app: Flask):
    if app.config['ENV'] == 'development':
        app.config.from_object(DevelopmentConfig)
    elif app.config['ENV'] == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)
    #
    # This sets the max size to the default: 64 MB
    #
    patch_request_class(app)
    configure_uploads(app, IMAGE_SET)


def register_extensions(app: Flask):
    """Register Flask extensions."""
    db.init_app(app)
    Migrate(app, db, render_as_batch=True)
    ma.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    set_jwt_loaders()
    return None

def set_jwt_loaders():
    """
    `claims` are data we choose to attach to each jwt payload
    and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
    one possible use case for claims are access level control, which is shown below.
    """
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
        if identity == 1:   # instead of hard-coding, we should read from a config file or database to get a list of admins instead
            return {'is_admin': True}
        return {'is_admin': False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        BlacklistedToken(jti=jti).save_to_db()
        raise ExpiredTokenError

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        raise InvalidTokenError

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        raise MissingTokenError
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        raise StaleTokenError

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        raise RevokedTokenError

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return BlacklistedToken.find_by_jti(jti)


def configure_logger(app: Flask):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)