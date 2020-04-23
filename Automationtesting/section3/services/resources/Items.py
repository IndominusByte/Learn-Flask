from flask_restful import Resource, request
from services.models.ItemsModel import ItemModel
from services.schemas.ItemSchema import ItemSchema

item_schema = ItemSchema()

class CrudItem(Resource):
    def get(self,name: str):
        item = ItemModel.query.filter_by(name=name).first_or_404(description='Upps name not found!')
        return item_schema.dump(item), 200

    def post(self,name: str):
        data = request.get_json()
        args = item_schema.load(data)
        item = ItemModel(args['name'],args['price'],args['store_id'])
        item.save_to_db()
        return {"message":f"{item.name} success to save"}, 201

    def put(self,name: str):
        item = ItemModel.query.filter_by(name=name).first_or_404(description='Upps name not found!')
        data = request.get_json()
        args = item_schema.load(data)
        item.name = args['name']
        item.price = args['price']
        item.store_id = args['store_id']
        item.save_to_db()
        return {"message":"item success to update"}, 200

    def delete(self,name: str):
        item = ItemModel.query.filter_by(name=name).first_or_404(description='Upps name not found!')
        item.delete_from_db()
        return {"message":"item success deleted"}, 200

class AllItem(Resource):
    def get(self):
        item_schema = ItemSchema(many=True,exclude=("store_id",))
        item = ItemModel.query.all()
        return item_schema.dump(item)
