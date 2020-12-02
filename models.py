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


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer)
    state = db.Column(db.String(50), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    date_inserted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False)
    user_phone_nr = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)



if __name__ == '__main__':
    db.create_all()