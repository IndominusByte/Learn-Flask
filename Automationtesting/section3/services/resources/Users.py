from flask_restful import Resource, request
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError
from services.models.UserModel import UserModel
from services.schemas.UserSchema import UserSchema

user_schema = UserSchema()

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        args = user_schema.load(data)
        if UserModel.query.filter_by(username=args['username']).first():
            raise ValidationError({'username':['Username cannot be duplicated']})
        user = UserModel(**args)
        user.save_to_db()
        return {"message":f"{user.username} succcess added"}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        args = user_schema.load(data)
        user = UserModel.query.filter_by(username=args['username']).first()
        if user and user.check_pass(args['password']):
            ret = {
                'access_token':create_access_token(identity=user.id,fresh=True),
                'refresh_token':create_refresh_token(identity=user.id)
            }
            return ret, 200
        return {"error":"Invalid credential"}, 400

class UserDelete(Resource):
    def delete(self,username: str):
        user = UserModel.query.filter_by(username=username).first_or_404(description="data not found!")
        user.delete_from_db()
        return {"message":f"{user.username} has been delete"}, 200
