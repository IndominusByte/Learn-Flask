import re
from typing import Dict
from services import jwt, db
from services.models import User, ConfirmationUser
from marshmallow import ValidationError
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_raw_jwt,
    get_jwt_identity,
    jwt_required,
    jwt_refresh_token_required,
    fresh_jwt_required
)
from services.blacklists import blacklists
from services.schemas import UserSchema
from services.libs.mailgun import MailGunException

_schema = UserSchema()

class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        args = _schema.load(data)
        errors = self._errors(args)
        if errors: return errors, 400
        user = User(**args)
        try:
            user.save_to_db()
            confirmation = ConfirmationUser(user.id)
            confirmation.save_to_db()
            confirmation.send_email_confirmation()
        except MailGunException as err:
            user.delete_from_db()
            return {'error':str(err)}, 400

        return {'success':f'User {user.username} success created'}, 200

    @staticmethod
    def _errors(args: Dict) -> None:
        errors = {}
        if User.query.filter_by(username=args['username']).first(): errors['username'] = 'Username has been taken!'
        if User.query.filter_by(email=args['email']).first(): errors['email'] = 'Email has been taken!'
        return errors

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        args = _schema.load(data,partial=("username",))
        user = User.query.filter_by(email=args['email']).first()
        if user and user.check_pass(args['password']):
            if user.confirmation.activated:
                access_token = create_access_token(identity=user.id,fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {'access_token':access_token,'refresh_token':refresh_token}, 200
            return {'error':'Your account not activated yet!'}, 400
        return {'error':'Username or password wrong!'}, 400

class ActivateUser(Resource):
    def get(self,token: str):
        confirmation = ConfirmationUser.filter_by_id(token)
        if confirmation:
            if not confirmation.expired_token:
                confirmation.activated = True
                confirmation.save_to_db()
                return {'message':f'Email {confirmation.user.email} has been activated'}, 200
            return {'message':'Token email expired!'}, 500
        return {'message':'Upps not found'}, 400

class ResendEmail(Resource):
    def post(self):
        data = request.get_json()
        args = _schema.load(data,partial=("password","username"))
        user = User.query.filter_by(email=args['email']).first_or_404(description="upps email not found!")
        if user and not user.confirmation.activated:
            try:
                user.confirmation.send_email_confirmation()
                user.confirmation.change_expired()
                user.confirmation.save_to_db()
                return {'message':'Email activated already send'}, 200
            except MailGunException as err:
                return {'error':str(err)}, 400

        return {'message':'Your email already activated'}, 200

class LogoutUser(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklists.add(jti)
        return {'success':'Successfully logged out'}, 200

class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        return {'access_token':new_token}, 200

class CrudUser(Resource):
    @jwt_required
    def get(self,user_id: int):
        schema = UserSchema(only=("id","username","email"))
        user = User.query.filter_by(id=user_id).first_or_404(description='User id not found!')
        return schema.dump(user), 200

    @fresh_jwt_required
    def put(self,user_id: int):
        data = request.get_json()
        args = _schema.load(data,partial=("password","email"))
        user = User.query.filter_by(id=user_id).first_or_404(description='User not found!')
        user.username = args['username']
        user.save_to_db()
        return {'success':f'success change {user.username} profile'}, 200
