#PUPPY TO MANY TOYS
#ONE PUPPY TO ONE OWNER

'''
puppies -> id,name, add func report_toys
toys -> id,item_name
owners -> id,name
'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'relationship.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Puppy(db.Model):
    __tablename__ = 'puppies'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    #relationship one to many
    toys = db.relationship('Toy',backref='puppy',lazy='dynamic')
    #relationship one to one , add uselist=False
    owner = db.relationship('Owner',backref='puppy',uselist=False)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"{self.name} puppy has owner {self.owner.name}"
        else:
            return f"{self.name} puppy not has owner!"

    def report_toys(self):
        print(f'=== All toys inside {self.name} puppy')
        for toy in self.toys:
            print(toy.item_name)

class Toy(db.Model):
    __tablename__ = 'toys'

    id = db.Column(db.Integer,primary_key=True)
    item_name = db.Column(db.String(100))
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id'))

    def __init__(self,item_name,puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id

class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id'))

    def __init__(self,name,puppy_id):
        self.name = name
        self.puppy_id = puppy_id
