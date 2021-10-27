import os
from flask import request, url_for
from requests import Response, post

from claims_solutions_api.models import db
from claims_solutions_api.libs.mailgun import Mailgun


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    pw_hash = db.Column(db.LargeBinary, nullable=False)
    salt = db.Column(db.LargeBinary, nullable=False, default=os.urandom(32))
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_on = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    @classmethod
    def find_by_username(cls, username) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:
        #
        # - the "url_root" is "http://127.0.0.1:5000/"
        # - we're adding "userconfirm" to the root in order to get the endpoint
        #
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.id)
        
        return Mailgun.send_email(
            [self.email],
            "Claims Solutions Email Confirmation",
            f"Please click link to confirm your registration {link}",
            f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
