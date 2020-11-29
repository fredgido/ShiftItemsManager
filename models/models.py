from .main import db
from datetime import datetime

class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_description = db.Column(db.Text)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_nr = db.Column(db.Integer, unique=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    date_inserted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.Datetime, onupdate=datetime.utcnow)
    item_type_id = db.Column(db.Integer_db.ForeignKey(ItemType.id))


if __name__ == '__main__':
    db.create_all()
