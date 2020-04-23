from marshmallow import Schema, fields, validate, validates, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True,validate=validate.Length(min=6))

    @validates('username')
    def validate_username(self,data):
        if not data: raise ValidationError('Username cannot blank')

    @validates('password')
    def validate_password(self,data):
        if not data: raise ValidationError('Password cannot blank')
