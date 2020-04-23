from marshmallow import Schema, fields, validate, validates, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    avatar = fields.Str(dump_only=True)
    password = fields.Str(required=True,validate=validate.Length(min=6),load_only=True)
    confirmation = fields.Nested("ConfirmationSchema",exclude=("user",))
    items = fields.List(fields.Nested("ItemSchema",exclude=("user",)))

    @validates("username")
    def validate_username(self,value):
        if not value: raise ValidationError("Username cannot blank!")

    @validates("password")
    def validate_password(self,value):
        if not value: raise ValidationError("Password cannot blank!")
