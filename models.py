from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

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
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'), nullable=False)
    reservations = db.relationship('Reservation', backref='item', lazy=True)


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer)
    state = db.Column(db.String(50), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    date_inserted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    phone_nr = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    perms = db.Column(db.String(50), nullable=False)

    def __init__(self, username, phone_nr, email, password, perms):
        self.username = username
        self.phone_nr = phone_nr
        self.email = email
        self.password = password
        self.perms = perms

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)


if __name__ == '__main__':
    db.create_all()