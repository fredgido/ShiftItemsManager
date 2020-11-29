from flask import render_template, jsonify, request

from main import app, db
from models import Item, ItemType


@app.route("/test")
def test():
    item_type_list = [{"item_name": "Radio"}, {"item_name": "Baterias"}, {"item_name": "Chaves"}]
    return render_template('dashindex.html', item_type_list=item_type_list)


@app.route("/")
def index():
    item_type_list = [obj.__dict__ for obj in ItemType.query.all()]
    return render_template('dashindex.html', item_type_list=item_type_list)


@app.route("/item", methods=['GET'])
def item_list():
    objs = Item.query.all()
    return jsonify([obj.__dict__ for obj in objs])


@app.route("/item", methods=['POST'])
def item_save():
    new_item = db.Item(**request.form.__dict__)


@app.route("/item_type")
def item_type_list():
    return render_template('dashindex.html')
