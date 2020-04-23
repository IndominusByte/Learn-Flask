from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bcrpyt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = bcrpyt.generate_password_hash(password)

    def check_pass(self,password):
        return bcrpyt.check_password_hash(self.password,password)

class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self,name):
        self.name = name

    def get_json(self):
        return {'name':self.name}
