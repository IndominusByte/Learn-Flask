import string, random, uuid
from time import time
from flask import request, url_for
from requests import Response, post
from marshmallow import ValidationError
from typing import Dict, Union, ClassVar
from services import db, bcrypt
from services.libs.mailgun import Mailgun

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True)
    email = db.Column(db.String(100),unique=True,index=True)
    password = db.Column(db.String(100))
    items = db.relationship('Item',backref='user',cascade='all,delete-orphan')
    confirmation = db.relationship('ConfirmationUser',backref='user',uselist=False,cascade='all,delete-orphan')

    def __init__(self,username: str,email: str,password: str):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def check_pass(self,password: str) -> bool:
        return bcrypt.check_password_hash(self.password,password)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

class ConfirmationUser(db.Model):
    __tablename__ = 'confirmation_users'

    id = db.Column(db.String(100),primary_key=True)
    activated = db.Column(db.Boolean,default=False)
    expired_at = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self,user_id: int):
        self.id = uuid.uuid4().hex
        self.expired_at = int(time()) + 1800 # 30 menit
        self.user_id = user_id

    @classmethod
    def filter_by_id(self,token: str) -> 'ConfirmationUser':
        return self.query.get(token)

    @property
    def expired_token(self) -> bool:
        return int(time()) > self.expired_at

    def change_expired(self) -> None:
        self.expired_at = int(time()) + 1800 # 30 menit

    def send_email_confirmation(self) -> Response:
        link = request.url_root[:-1] + url_for('activateuser',token=self.id)
        return Mailgun.send_email([self.user.email],'Activated email','email.html',link=link,txt='tulisan')

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self,name: str,user_id: int):
        self.name = name
        self.user_id = user_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
