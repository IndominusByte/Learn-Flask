import os
from marshmallow import Schema, fields, ValidationError

ALLOW_FILE_EXT = ['jpg','png','jpeg']
MAX_FILE_SIZE = 500 * 1024  # 500kb

class ImageField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if not value:
            raise ValidationError("Image field cannot blank")

        if not value.filename.split('.')[-1] in ALLOW_FILE_EXT:
            raise ValidationError("Image must be {}".format('|'.join(ALLOW_FILE_EXT)))

        value.seek(0,os.SEEK_END)
        size = value.tell()

        if size > MAX_FILE_SIZE:
            raise ValidationError("Image cannot grater than 500 kb")

        value.seek(0)
        return value

class UploadImageSchema(Schema):
    image = ImageField(required=True)
