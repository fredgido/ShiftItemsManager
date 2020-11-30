from flask import render_template, jsonify, request

from main import app, db
from models import Item, ItemType
from utils import serialize


@app.route("/test")
def test():
    item_type_list = [{"item_name": "Radio"}, {"item_name": "Baterias"}, {"item_name": "Chaves"}]
    return render_template('dashindex.html', item_type_list=item_type_list)


@app.route("/")
def index():
    item_type_list = ItemType.query.all()
    return render_template('dashindex.html', item_type_list=item_type_list)


@app.route("/item", methods=['GET'])
def item_list():
    objs = serialize(Item.query.all())
    return jsonify(objs)


@app.route("/item", methods=['POST'])
def item_save():
    new_item = db.Item(**request.form.__dict__)


@app.route("/item_type")
def item_type_list():
    objs = ItemType.query.all()

    return jsonify(objs)
