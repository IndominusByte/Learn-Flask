from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from config import api,app,db
from models import Car

class CrudCar(Resource):
    def get(self,name):
        car = Car.query.filter_by(name=name).first_or_404()
        return car.get_json()

    def post(self,name):
        car = Car(name=name)
        db.session.add(car)
        db.session.commit()
        return {'message':f'success add {name}'}

    def delete(self,name):
        car = Car.query.filter_by(name=name).first_or_404()
        db.session.delete(car)
        db.session.commit()
        return {'message':f'success delete {name}'}

class CrudUser(Resource):
    def post(self):
        name = request.get_json()['name']
        password = request.get_json()['password']
        user = User(name,password)
        db.session.add(user)
        db.session.commit()
        return {'message':f'user {name} berhasil dibuat!'}

class Cars(Resource):
    @jwt_required()
    def get(self):
        cars = Car.query.all()
        return [x.get_json() for x in cars]

api.add_resource(CrudCar,'/car/<name>')
api.add_resource(Cars,'/cars')
api.add_resource(CrudUser,'/user')

if __name__ == '__main__':
    app.run(debug=True)
