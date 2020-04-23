from services.serve import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,index=True)

    items = db.relationship('ItemModel',backref='store',cascade='all,delete-orphan')

    def __init__(self,name: str):
        self.name = name

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
