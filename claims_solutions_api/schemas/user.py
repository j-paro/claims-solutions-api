from marshmallow import validate
from marshmallow.fields import String

from claims_solutions_api.schemas import ma


class UserSchema(ma.Schema):

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
            min=4,
            error="'username' doesn't comply with length requirment."
        )
    )
    email = String(
        validate=validate.Length(
            max=80,
            error="'username' doesn't comply with length requirment."
        )
    )
    