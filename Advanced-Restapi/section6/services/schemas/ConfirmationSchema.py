from marshmallow import Schema, fields

class ConfirmationSchema(Schema):
    id = fields.Str(dump_only=True)
    activated = fields.Boolean()
    expired_at = fields.Int()
    resend_expired = fields.Int()
    user = fields.Nested('UserSchema',only=("username","email",))
