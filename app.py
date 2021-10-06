from flask import Flask, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from db import db
from resources.company import Company, CompanyList
from ma import ma
from resources.errors import errors

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
api = Api(app, errors=errors)

@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

api.add_resource(Company, "/company/<string:name>")
api.add_resource(CompanyList, "/companies")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)