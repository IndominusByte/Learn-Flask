from marshmallow import ValidationError
from sqlalchemy import orm
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.schemas import ItemSchema, UserSchema, UserConfirmation
from services.models import Item, User

_schema = ItemSchema()

class CrudItem(Resource):
    @jwt_required
    def get(self):
        schema = UserSchema()
        user = User.query.get(get_jwt_identity())
        item = Item.query.options(orm.joinedload('user')).all()
        return schema.dump(user), 200

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        result = _schema.load(data)
        item = Item(result['name'],user_id)
        item.save_to_db()
        return {"success":f"item {item.name} successfully save"}, 200
