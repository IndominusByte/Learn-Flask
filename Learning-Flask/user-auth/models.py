from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bycrpt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(125),unique=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = bycrpt.generate_password_hash(password)

    def check_password(self,password):
        return bycrpt.check_password_hash(self.password,password)
