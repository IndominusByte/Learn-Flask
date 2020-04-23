from services.serve import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True,index=True)
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer,db.ForeignKey('stores.id'),nullable=False)

    def __init__(self,name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
