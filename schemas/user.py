from marshmallow import validate
from marshmallow.fields import String

from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "activated")
        load_instance = True

    id = ma.auto_field()
    username = String(
        required=True,
        validate=validate.Length(
            min=1,
            max=80,
            error="'username' doesn't comply with length requirment."
        )
    )
    password = String(
        required=True,
        validate=validate.Length(
            min=1,
            error="'username' doesn't comply with length requirment."
        )
    )
    activated = ma.auto_field()
