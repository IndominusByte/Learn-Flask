import os
from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api
from flask_cors import CORS
from models import db, migrate, Car, User, bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app,db)
bcrypt.init_app(app)

def authenticated(username,password):
    user = User.query.filter_by(name=username).first()
    if user and user.check_pass(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

jwt = JWT(app,authenticated,identity)

class CreateUser(Resource):
    def post(self):
        req = request.get_json(force=True)
        user = User(req['username'],req['password'])
        db.session.add(user)
        db.session.commit()
        return {'message':'user berhasil dibuat!'}

class CarCrud(Resource):
    def get(self,name):
        car = Car.query.filter_by(name=name).first_or_404(description='There is no data with {}'.format(name))
        return car.json()

    def post(self,name):
        car = Car(name)
        db.session.add(car)
        db.session.commit()
        return {'message':'data berhasil dimasukan!'}

    def delete(self,name):
        car = Car.query.filter_by(name=name).first_or_404(description='There is no data with {}'.format(name))
        db.session.delete(car)
        db.session.commit()
        return {'message':'data telah terhapus!'}

class AllCar(Resource):
    @jwt_required()
    def get(self):
        car = Car.query.all()
        return [x.json() for x in car]

api.add_resource(CarCrud,'/car/<name>')
api.add_resource(AllCar,'/cars')
api.add_resource(CreateUser,'/add/user')

'''
class User():
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

users = [ User(1,'oman','password'),User(2,'pradipta','secret') ]

username_table = {x.username: x for x in users}
userid_table = {x.id: x for x in users}

def authenticated(username,password):
    user = username_table.get(username,None)
    if user and password == user.password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id,None)

jwt = JWT(app,authenticated,identity)

puppies = []
class Puppy(Resource):
    def get(self,name):
        for item in puppies:
            if item['name'] == name:
                return item

        return {'status':'upps not found!'},404

    def post(self,name):
        puppies.append({'name':name})
        return {'name':name}

    def delete(self,name):
        for key,value in enumerate(puppies):
            if value['name'] == name:
                puppies.pop(key)
                return {'status':f'{name} has been delete'}

        return {'status':'upps not found!'},404

class PuppiesAll(Resource):
    @jwt_required()
    def get(self):
        return puppies

api.add_resource(Puppy,'/puppy/<name>')
api.add_resource(PuppiesAll,'/puppies')
'''

if __name__ == '__main__':
    app.run(debug=True,host='192.168.1.40')
