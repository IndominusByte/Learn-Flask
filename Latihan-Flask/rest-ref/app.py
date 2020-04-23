import os, re
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from models import Car, User, db, bcrpyt, migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)
migrate.init_app(app,db)
bcrpyt.init_app(app)

def authenticated(email,password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_pass(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

jwt = JWT(app,authenticated,identity)

class CrudUser(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument(
            'name',
            type=str,
            required=True,
            help="Name cannot blank",
            location='json'
            )
    parser.add_argument(
            'email',
            type=str,
            required=True,
            help="Email cannot blank",
            location='json'
            )

    parser.add_argument(
            'password',
            type=str,
            required=True,
            help="Password cannot blank",
            location='json'
            )

    def post(self):
        res = self.parser.parse_args()
        if not re.match(r"[^@]+@[^@]+\.[^@]+",res['email']): return jsonify({"message":"Format email wrong!"})
        if len(res['password']) < 6: return jsonify({"message":"password at least 6 character"})
        user = User(res['name'],res['email'],res['password'])
        db.session.add(user)
        db.session.commit()
        return {'message':'user {} has been saved'.format(user.name)}

class CrudCar(Resource):
    def get(self,name):
        car = Car.query.filter_by(name=name).first_or_404(description='data not found!')
        return {'name':car.name}
    def post(self,name):
        car = Car(name)
        db.session.add(car)
        db.session.commit()
        return {'message':'data success saved!'}

class AllCar(Resource):
    @jwt_required()
    def get(self):
        cars = Car.query.all()
        data = [x.get_json() for x in cars]
        return data

class Protected(Resource):
    @jwt_required()
    def get(self):
        return jsonify({
            "name":current_identity.name,
            "email":current_identity.email,
            })

api.add_resource(CrudCar,'/car/<name>')
api.add_resource(AllCar,'/car')
api.add_resource(Protected,'/')
api.add_resource(CrudUser,'/user')

if __name__ == '__main__':
    app.run(debug=True)
