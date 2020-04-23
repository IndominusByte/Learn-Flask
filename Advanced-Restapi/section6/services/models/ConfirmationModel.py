import uuid
from time import time
from flask import request, url_for
from services.config import db
from services.libs.MailSmtp import MailSmtp

class Confirmation(db.Model):
    __tablename__ = 'confirmation_users'

    id = db.Column(db.String(100),primary_key=True)
    activated = db.Column(db.Boolean,default=False)
    expired_at = db.Column(db.Integer)
    resend_expired = db.Column(db.Integer,nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self,user_id: int):
        self.id = uuid.uuid4().hex
        self.expired_at = int(time()) + 1800  # add 30 minute
        self.user_id = user_id

    def send_email_confirm(self) -> None:
        link = request.url_root[:-1] + url_for('confirmuser',token=self.id)
        MailSmtp.send_email([self.user.email],'Activated User','mail.html',link=link,username=self.user.username)

    @property
    def not_expired(self) -> bool:
        return self.expired_at > int(time())

    @property
    def resend_is_expired(self) -> bool:
        return int(time()) > self.resend_expired

    def generate_resend_expired(self) -> None:
        self.resend_expired = int(time()) + 900  # add 15 minute

    def change_expired(self) -> None:
        self.expired_at = int(time()) + 1800  # add 30 minute

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
