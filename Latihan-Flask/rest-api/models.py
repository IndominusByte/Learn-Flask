from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self,name,password):
        self.name = name
        self.password = bcrypt.generate_password_hash(password)

    def check_pass(self,password):
        return bcrypt.check_password_hash(self.password,password)


class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

    def get_json(self):
        return {'name':self.name}
