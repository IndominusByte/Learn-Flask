from datetime import datetime
from slugify import slugify
from flask_login import UserMixin
from services import db, login_manager, bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),unique=True,index=True)
    username = db.Column(db.String(100),unique=True,index=True)
    password = db.Column(db.String(100))
    avatar = db.Column(db.String(100),default='default.png')
    post = db.relationship('Post',backref='user',lazy='dynamic',cascade='all, delete, delete-orphan')

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(password)

    def check_pass(self,password):
        return bcrypt.check_password_hash(self.password,password)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.slug = slugify(title)
        self.text = text
        self.user_id = user_id
