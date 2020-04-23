from flask_sqlalchemy import orm
from flask_restful import Resource, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_raw_jwt,
    get_jwt_identity,
    fresh_jwt_required,
    jwt_required,
    jwt_refresh_token_required
)
from services.schemas.UserSchema import UserSchema
from services.models.UserModel import User
from services.models.ConfirmationModel import Confirmation
from services.libs.MailSmtp import MailSmtpException
from services.blacklist import blacklist

user_schema = UserSchema()

class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        args = user_schema.load(data)
        errors = RegisterUser.check_duplicate(args)
        if errors: return {"error":errors}, 400
        user = User(**args)
        user.save_to_db()
        try:
            confirm = Confirmation(user.id)
            confirm.save_to_db()
            confirm.send_email_confirm()
        except MailSmtpException as err:
            user.delete_from_db()
            return {"error":str(err)}, 400

        return {"message":"User has been created"}, 201

    @staticmethod
    def check_duplicate(args):
        errors = {}
        if User.query.filter_by(username=args['username']).first(): errors['username'] = 'Username already exists!'
        if User.query.filter_by(email=args['email']).first(): errors['email'] = 'Email already exists!'
        return errors

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        args = user_schema.load(data,partial=("username",))
        user = User.query.filter_by(email=args['email']).first()
        if user and user.check_pass(args['password']):
            if user.confirmation.activated:
                ret = {
                    'access_token':create_access_token(identity=user.id,fresh=True),
                    'refresh_token':create_refresh_token(identity=user.id)
                }
                return ret, 200
            return {"error":"You must activated you user!"}, 400
        return {"error":"Invalid credential"}, 400

class LogoutUser(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {'message':'Succesfully logged out'}, 200

class ConfirmUser(Resource):
    def get(self,token: str):
        confirm = Confirmation.query.filter_by(id=token).first_or_404(description="Data not found!")
        if confirm and not confirm.activated:
            if confirm.not_expired:
                confirm.activated = True
                confirm.save_to_db()
                return {"message":f"Your email {confirm.user.email} has been activated"},200
            return {"message":"Upps token expired you can resend email confirm again"}, 400
        return {"message":"Your account already activated"}, 200

class ResendEmail(Resource):
    def post(self):
        data = request.get_json()
        args = user_schema.load(data,partial=("username","password",))
        user = User.query.filter_by(email=args['email']).first_or_404(description="Data not found")
        if user and not user.confirmation.activated:
            if not user.confirmation.resend_expired or user.confirmation.resend_is_expired:
                try:
                    user.confirmation.send_email_confirm()
                    user.confirmation.change_expired()
                    user.confirmation.generate_resend_expired()
                    user.confirmation.save_to_db()
                    return {"message":"Email confirmation has send"}, 200
                except MailSmtpException as err:
                    return {"error":str(err)}, 400

            return {"error":"You can try 15 minute later"}, 400
        return {"message":"Your account already activated"}, 200

class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id,fresh=False)
        return {'access_token':new_token}, 200

class UpdateUser(Resource):
    @fresh_jwt_required
    def put(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        args = user_schema.load(data,partial=("email","password",))
        user = User.query.get(user_id)
        user.username = args['username']
        user.save_to_db()
        return {"message":"Success update your profile"}, 200

class GetUser(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.options(orm.joinedload('items')).get(user_id)
        return user_schema.dump(user), 200
