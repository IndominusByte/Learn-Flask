from flask_sqlalchemy import orm
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.schemas.ItemSchema import ItemSchema
from services.models.ItemModel import Item

item_schema = ItemSchema()

class CrudItem(Resource):
    def get(self):
        schema = ItemSchema(exclude=['user'],many=True)
        item = Item.query.options(orm.joinedload('user')).all()
        return schema.dump(item), 200

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        args = item_schema.load(data)
        if Item.query.filter_by(name=args['name']).first(): return {"error":"Name already exists"}, 400
        item = Item(args['name'],user_id)
        item.save_to_db()
        return {"message":"Successfully add item"}, 200
