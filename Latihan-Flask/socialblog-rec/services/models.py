from services import db, migrate, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime
from slugify import slugify

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True)
    email = db.Column(db.String(100),unique=True,index=True)
    password = db.Column(db.String(100))
    avatar = db.Column(db.String(100),default='default.png')
    created_at = db.Column(db.DateTime,default=datetime.now)
    updated_at = db.Column(db.DateTime,default=datetime.now)

    post = db.relationship('Post',backref='user',lazy='dynamic',cascade='all,delete,delete-orphan')

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def check_pass(self,password):
        return bcrypt.check_password_hash(self.password,password)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100),unique=True,index=True)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime,default=datetime.now)
    updated_at = db.Column(db.DateTime,default=datetime.now)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.slug = slugify(title)
        self.text = text
        self.user_id = user_id
