from flask_restful import Resource
from flask import request, make_response, render_template
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from claims_solutions_api.models.blacklisted_token import BlacklistedToken

from claims_solutions_api.models.user import UserModel
from claims_solutions_api.schemas.user import UserSchema
from claims_solutions_api.errors import (
    UnauthorizedError,
    UserNotConfirmedError,
    UserNotFoundError,
    InternalServerError
)
from claims_solutions_api.messages import SuccessMessage
from claims_solutions_api.security.password import Password

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        #
        # Validation errors get handled by handler specified in "app.py"
        #
        user = user_schema.load(request.get_json())
        username=user['username']

        if UserModel.find_by_username(username):
            raise UnauthorizedError

        pw = Password(user['password'])
        saved_user = UserModel(
            username=username,
            pw_hash=pw.hash,
            salt=pw.salt,
            email=user['email']
        )

        try: 
            saved_user.save_to_db()
            saved_user.send_confirmation_email()
        except:
            raise InternalServerError

        return SuccessMessage(
            "user",
            username,
            "create",
            user_schema.dump(user)
        ).get_msg(), 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        #
        # Validation errors get handled by handler specified in "app.py"
        #
        input = user_schema.load(request.get_json())

        user = UserModel.find_by_username(input['username'])
        if user:
            input_pw = Password(input['password'], user.salt)
            if user.pw_hash == input_pw.hash:
                if user.activated:
                    access_token = create_access_token(
                        identity=user.id,
                        fresh=True
                    )
                    refresh_token = create_refresh_token(user.id)
                    return SuccessMessage(   
                        "user",
                        user.username,
                        "login",
                        {
                            "access_token": access_token,
                            "refresh_token": refresh_token
                        }
                    ).get_msg(), 200
                raise UserNotConfirmedError

        raise UnauthorizedError


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti']
        BlacklistedToken(jti=jti).save_to_db()

        user_id = get_jwt_identity()
        return SuccessMessage(
            "user",
            user_id,
            "logout",
            {"user_id": user_id}
        ).get_msg(), 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return SuccessMessage(   
            "user",
            current_user,
            "token refresh",
            {"access_token": new_token}
        ).get_msg(), 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.activated = True
            user.save_to_db()
            return make_response(
                render_template('confirmation_page.html', email=user.username),
                200,
                {'Content-Type': 'text/html'}
            )
        
        raise UnauthorizedError


#
# Used only for development
#
class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to 
    expose it to public users, but for the sake of demonstration in this course,
    it can be useful when we are manipulating user_data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            raise UserNotFoundError
        return SuccessMessage(
            "user",
            user_id,
            "search",
            user_schema.dump(user)
        ).get_msg(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            raise UserNotFoundError
        user.delete_from_db()
        return SuccessMessage(
            "user",
            user.username,
            "delete",
            user_schema.dump(user)
        ).get_msg(), 200