import os
import traceback
from flask import request, send_file, current_app
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import safe_join

from claims_solutions_api.libs import image_helper
from claims_solutions_api.schemas.image import ImageSchema
from claims_solutions_api.messages import SuccessMessage
from claims_solutions_api.errors import (
    IllegalImageError,
    IllegalFilenameError,
    ImageNotFoundError,
    InternalServerError
)


image_schema = ImageSchema()


class ImageUpload(Resource):
    @jwt_required()
    def post(self):
        """
        This endpoint is used to upload an image file. It uses the JWT to
        retrieve user information and save the image in the user's folder. If a
        file with the same name exists in the user's folder, name conflicts will
        will be automatically resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).
        """
        #
        # "request.files" is a dictionary of filename -> "FileStorage"
        #
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        try:
            image_path = image_helper.save_image(data['image'], folder=folder)
            basename = image_helper.get_basename(image_path)
            return SuccessMessage(
                'image',
                basename,
                'upload',
                '<image>'
            ).get_msg(), 201
        except UploadNotAllowed:
            raise IllegalImageError


class Image(Resource):
    @jwt_required()
    def get(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not image_helper.is_filename_safe(filename):
            raise IllegalFilenameError

        try:
            #
            # I couldn't just send the "image_path" into "send_file". Doing that
            # got an incorrect path which resulted in a "FileNotFoundError".
            #
            image_path = image_helper.get_path(filename, folder=folder)
            return send_file(os.path.abspath(image_path))
        except FileNotFoundError:
            traceback.print_exc()
            raise ImageNotFoundError

    @jwt_required()
    def delete(self, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not image_helper.is_filename_safe(filename):
            raise IllegalFilenameError

        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return SuccessMessage(
                'image',
                filename,
                'delete',
                '<image>'
            ).get_msg(), 200
        except FileNotFoundError:
            traceback.print_exc()
            raise ImageNotFoundError
        except:
            traceback.print_exc()
            raise InternalServerError