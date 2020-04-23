from marshmallow import Schema, fields, validates, validate, ValidationError

class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    user = fields.Nested("UserSchema",only=("id","username"))

    @validates("name")
    def validate_name(self,data):
        if not data: raise ValidationError("gk boleh null sat")

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True,validate=validate.Length(min=6))
    items = fields.List(fields.Nested("ItemSchema",exclude=("user",)))
    confirmation = fields.Nested("UserConfirmation",exclude=("user",))
