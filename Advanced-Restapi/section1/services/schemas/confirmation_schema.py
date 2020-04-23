from marshmallow import Schema, fields

class UserConfirmation(Schema):
    id = fields.Str()
    activated = fields.Int()
    expired_at = fields.Int()
    user = fields.Nested("UserSchema",only=("username","email"))
