from main import db
from datetime import datetime

class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_description = db.Column(db.Text)
    items = db.relationship('Item', backref='item_type', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_nr = db.Column(db.Integer, unique=True, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    date_inserted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'), nullable=False)


if __name__ == '__main__':
    db.create_all()