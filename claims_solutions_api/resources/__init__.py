import os
from flask_restful import Api

from claims_solutions_api.resources.company import Company, CompanyList
from claims_solutions_api.resources.user import (
    User,
    UserRegister,
    UserConfirm,
    UserLogin,
    UserLogout,
    TokenRefresh
)
from claims_solutions_api.resources.image import ImageUpload, Image
from claims_solutions_api.errors import errors

api = Api(errors=errors)

if os.environ['FLASK_ENV'] == 'development':
    api.add_resource(User, "/user/<int:user_id>")

api.add_resource(Company, "/company/<string:name>")
api.add_resource(CompanyList, "/companies")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")