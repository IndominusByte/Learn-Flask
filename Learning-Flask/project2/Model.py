from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

class Puppy(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    owner = db.relationship('Owner',backref='puppy',uselist=False,cascade="all, delete, delete-orphan")

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"puppy name is {self.name} and owner is {self.owner.name}"
        else:
            return f"puppy name is {self.name} and has no owner assignet yet!"

class Owner(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppy.id'),nullable=False)

    def __init__(self,name,id):
        self.name = name
        self.puppy_id = id

    def __repr__(self):
        return f"now owner {self.name} is linked to {self.puppy.name}"
