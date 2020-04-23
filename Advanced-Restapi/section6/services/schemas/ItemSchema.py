from marshmallow import Schema, fields, validates, ValidationError

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    user = fields.Nested('UserSchema',only=("username","email",))

    @validates("name")
    def validate_name(self,value):
        if not value: raise ValidationError("Name cannot blank!")
