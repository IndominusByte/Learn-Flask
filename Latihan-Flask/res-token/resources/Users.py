import re
from config import db, jwt
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    fresh_jwt_required,
    get_jwt_identity,
    get_jwt_claims,
    get_raw_jwt
)
from models import User
from blacklist import blacklists

class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = User.query.get(get_jwt_identity())
        new_token = create_access_token(identity=user.id,fresh=False)
        return {'access_token':new_token}, 200

class LogoutUser(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklists.add(jti)
        return {'success':'Successfully logged out'}, 200

class RegisterUser(Resource):
    _parser = reqparse.RequestParser(bundle_errors=True)
    _parser.add_argument('username',type=str,location='json',required=True,help='Username cannot blank!')
    _parser.add_argument('email',type=str,location='json',required=True,help='Email cannot blank!')
    _parser.add_argument('password',type=str,location='json',required=True,help='password cannot blank!')

    def post(self):
        args = self._parser.parse_args()
        errors = self._make_errors(args)
        if errors: return {"message":errors}, 400
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return {'success':'Success create user {}'.format(user.username)}, 201

    @staticmethod
    def _make_errors(args):
        errors = {}
        if User.query.filter_by(username=args['username']).first(): errors['username'] = 'Username already exists!'
        if User.query.filter_by(email=args['email']).first(): errors['email'] = 'Email already exists!'
        if not re.match(r"[^@]+@[^@]+\.[^@]+",args['email']): errors['email'] = 'Invalid email address'
        if len(args['password']) < 6: errors['password'] = 'Password at least 6 characters'
        return errors

class LoginUser(Resource):
    _parser = reqparse.RequestParser(bundle_errors=True)
    _parser.add_argument('email',type=str,location='json',required=True,help='Email cannot blank!')
    _parser.add_argument('password',type=str,location='json',required=True,help='password cannot blank!')

    def post(self):
        args = self._parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if user and user.check_pass(args['password']):
            ret = {
                    'access_token':create_access_token(identity=user.id,fresh=True),
                    'refresh_token':create_refresh_token(identity=user.id)
                }
            return ret, 200
        return {'failed':'Username or password wrong!'}, 401

class UpdateDeleteUser(Resource):
    _parser = reqparse.RequestParser(bundle_errors=True)
    _parser.add_argument('username',type=str,location='json',required=True,help='Username cannot blank!')

    @jwt_required
    def get(self,id):
        claims = get_jwt_claims()
        print(get_jwt_identity())
        return claims

    @fresh_jwt_required
    def put(self,id: int):
        args = self._parser.parse_args()
        user = User.query.filter_by(id=id).first_or_404(description='User not found!')
        user.username = args['username']
        db.session.add(user)
        db.session.commit()
        return {'success':'User hasbeed updated!'}, 200

    @jwt_required
    def delete(self,id: int):
        user = User.query.filter_by(id=id).first_or_404(description='User not found!')
        db.session.delete(user)
        db.session.commit()
        return {'success':'User {} has been delete'.format(user.username)}, 200
