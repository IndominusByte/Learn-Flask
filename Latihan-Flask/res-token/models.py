from config import db, migrate, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True)
    email = db.Column(db.String(100),unique=True,index=True)
    password = db.Column(db.String(100))

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def check_pass(self,password):
        return bcrypt.check_password_hash(self.password,password)
