from typing import Any, Optional, Mapping
from marshmallow import fields
from werkzeug.datastructures import FileStorage

from claims_solutions_api.schemas import ma


class FileStorageField(fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid image'
    }

    def _deserialize(
        self,
        value: Any,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs
    ) -> FileStorage:
        if value is None:
            return None
        
        if not isinstance(value, FileStorage):
            #
            # The following raises a ValidationError
            #
            self.fail('invalid')

        return value


class ImageSchema(ma.Schema):
    image = FileStorageField(required=True)