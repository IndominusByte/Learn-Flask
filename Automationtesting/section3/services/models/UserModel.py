from services.serve import db, bcrypt

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True)
    password = db.Column(db.String(100))

    def __init__(self,username: str,password: str):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)

    def check_pass(self,password: str) -> bool:
        return bcrypt.check_password_hash(self.password,password)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
