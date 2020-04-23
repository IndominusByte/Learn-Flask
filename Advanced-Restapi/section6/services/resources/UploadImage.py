import uuid, os
from flask import send_file
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.models.UserModel import User
from services.schemas.UploadImageSchema import UploadImageSchema

image_schema = UploadImageSchema()
dirname = os.path.join(os.path.dirname(__file__),'../static')

class UploadImage(Resource):
    @jwt_required
    def post(self):
        image = image_schema.load(request.files)
        ext = image['image'].filename.split('.')[-1]
        filename = uuid.uuid4().hex + '.' + ext
        image['image'].save(os.path.join(dirname,'images',filename))
        image['image'].close()
        return {'message':f'File {filename} success uploaded'}, 200

class Image(Resource):
    @jwt_required
    def get(self,filename: str):
        dirfile = os.path.join(dirname,'images',filename)
        try:
            return send_file(dirfile)
        except FileNotFoundError:
            return {"error":"File not found!"}, 404

    @jwt_required
    def delete(self,filename: str):
        dirfile = os.path.join(dirname,filename)
        try:
            os.remove(dirfile)
            return {"message":f"File {filename} successfully remove"}, 200
        except FileNotFoundError:
            return {"error":"File not found!"}, 404

class AvatarUpload(Resource):
    @jwt_required
    def put(self):
        image = image_schema.load(request.files)
        user = User.query.get(get_jwt_identity())
        # Delete image when user doesn't have default png
        if user.avatar != 'default.png':
            os.remove(os.path.join(dirname,'avatar',user.avatar))
        ext = image['image'].filename.split('.')[-1]
        filename = uuid.uuid4().hex + '.' + ext
        image['image'].save(os.path.join(dirname,'avatar',filename))
        image['image'].close()
        # Save filename to database
        user.avatar = filename
        user.save_to_db()
        return {"message":"Avatar has been uploaded!"}, 200

class Avatar(Resource):
    @jwt_required
    def get(self):
        user = User.query.get(get_jwt_identity())
        dirfile = os.path.join(dirname,'avatar',user.avatar)
        try:
            return send_file(dirfile)
        except FileNotFoundError:
            return {"error":"File not found!"}, 400
