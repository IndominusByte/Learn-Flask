from services.config import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True,index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self,name: str, user_id: int):
        self.name = name
        self.user_id = user_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
