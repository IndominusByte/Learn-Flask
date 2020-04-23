from marshmallow import Schema,fields,validates, ValidationError
from services.models.ItemsModel import ItemModel

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)
    store = fields.Nested("StoreSchema",only=("id","name"))

    @validates('name')
    def validate_name(self,data):
        if not data: raise ValidationError('Name cannot blank')
        if ItemModel.query.filter_by(name=data).first(): raise ValidationError('Name cannot be duplicate')

    @validates('price')
    def validate_price(self,data):
        if not data: raise ValidationError('Price cannot blank')
