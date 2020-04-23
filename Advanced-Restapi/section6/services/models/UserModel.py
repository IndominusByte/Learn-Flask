from services.config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True)
    email = db.Column(db.String(100),unique=True,index=True)
    avatar = db.Column(db.String(100),default='default.png')
    password = db.Column(db.String(100))
    confirmation = db.relationship('Confirmation',backref='user',uselist=False,cascade='all,delete-orphan')
    items = db.relationship('Item',backref='user',cascade='all,delete-orphan')

    def __init__(self,username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_pass(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password,password)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
