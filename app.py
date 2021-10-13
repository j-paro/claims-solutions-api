import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from db import db
from resources.company import Company, CompanyList
from resources.user import (
    User,
    UserRegister,
    UserConfirm,
    UserLogin,
    UserLogout,
    TokenRefresh
)
from ma import ma
from errors import errors
from config import DevelopmentConfig, ProductionConfig

################################################################################
# Flask App
################################################################################
app = Flask(__name__)
if app.config['ENV'] == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

@app.before_first_request
def create_tables():
    db.create_all()

#
# This response is "jsonify'ed" because I think the response doesn't go thru the
# the api... Again, I think.
#
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

################################################################################
# JWT Manager
################################################################################
jwt = JWTManager(app)

################################################################################
# Flask RESTful API
################################################################################
api = Api(app, errors=errors)

if app.config['ENV'] == 'development':
    api.add_resource(User, "/user/<int:user_id>")

api.add_resource(Company, "/company/<string:name>")
api.add_resource(CompanyList, "/companies")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")

################################################################################
# main
################################################################################
if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)