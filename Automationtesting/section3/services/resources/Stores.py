from flask_restful import Resource
from flask_jwt_extended import jwt_required
from services.models.StoreModel import StoreModel
from services.schemas.StoreSchema import StoreSchema

store_schema = StoreSchema()

class CrudStore(Resource):
    def get(self,name: str):
        store = StoreModel.query.filter_by(name=name).first_or_404(description="Data not found")
        return store_schema.dump(store), 200

    @jwt_required
    def post(self,name: str):
        if StoreModel.query.filter_by(name=name).first(): return {"error":"Name cannot be duplicate"}, 400
        store = StoreModel(name)
        store.save_to_db()
        return {"message":f"{store.name} successfully added"}, 201

    @jwt_required
    def delete(self,name: str):
        store = StoreModel.query.filter_by(name=name).first_or_404(description="Data not found")
        store.delete_from_db()
        return {"message":"success from delete"}, 200

class AllStore(Resource):
    @jwt_required
    def get(self):
        store = StoreModel.query.all()
        store_schema = StoreSchema(many=True)
        return store_schema.dump(store), 200
