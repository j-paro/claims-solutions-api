from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)

from models.user import UserModel
from schemas.user import UserSchema
from errors import UnauthorizedError, UserNotConfirmedError
from resources.messages import SuccessMessage

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod    
    def post(cls):
        #
        # Validation errors get handled by handler specified in "app.py"
        #
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            raise UnauthorizedError

        user.save_to_db()

        return SuccessMessage(
            "user",
            user.username,
            "create",user_schema.dump(user)
        ).__dict__, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        #
        # Validation errors get handled by handler specified in "app.py"
        #
        user_data = user_schema.load(request.get_json())

        user = UserModel.find_by_username(user_data.username)

        #
        # this is what the `authenticate()` function did in security.py
        #
        if user:
            if safe_str_cmp(user.password, user_data.password):
                if user.activated:
                    #
                    # identity= is what the identity() function did in
                    # security.py—now stored in the JWT
                    #
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
                    ).__dict__, 200
                raise UserNotConfirmedError

        raise UnauthorizedError


class UserLogout(Resource):
    @classmethod    
    @jwt_required()
    def post(cls):
        user_id = get_jwt_identity()
        return SuccessMessage(
            "user",
            user_id,
            "logout",
            {"user_id": user_id}
        ).__dict__, 200


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
        ).__dict__, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.activated = True
            user.save_to_db()
            return SuccessMessage(   
                "user",
                user_id,
                "confirmation",
                user_schema.dump(user)
            ).__dict__, 200
        
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
            raise UnauthorizedError
        return SuccessMessage(
            "user",
            user_id,
            "search",
            user_schema.dump(user)
        ).__dict__, 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            raise UnauthorizedError
        user.delete_from_db()
        return SuccessMessage(
            "user",
            user.username,
            "delete",
            user_schema.dump(user)
        ).__dict__, 200