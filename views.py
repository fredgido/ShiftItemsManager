from flask import render_template, jsonify, request

from main import app, db
from models import Item, ItemType
from utils import serialize


@app.route("/test")
def test():
    all_item_type = [{"item_name": "Radio"}, {"item_name": "Baterias"}, {"item_name": "Chaves"}]
    return render_template('dashindex.html', item_type_list=all_item_type)


@app.route("/")
def index():
    all_item_type = ItemType.query.all()
    return render_template('dashindex.html', item_type_list=all_item_type)


@app.route("/item", methods=['GET'])
def item_list():
    objs = serialize(Item.query.all())
    return jsonify(objs)


@app.route("/item/<int:obj_id>", methods=['GET'])
def item_get(obj_id):
    objs = serialize(Item.query.get(obj_id))
    if objs:
        return jsonify(objs[0])
    return "not found", 404


@app.route("/item", methods=['POST'])
def item_save():
    try:
        new_item = Item(**request.form)
        db.session.add(new_item)
        db.session.commit()
    except BaseException as error:
        return str(error), 400
    return "success", 200


@app.route("/item_type")
def item_type_list():
    objs = serialize(ItemType.query.all())
    return jsonify(objs)


@app.route("/item_type/<int:obj_id>", methods=['GET'])
def item_type_get(obj_id):
    objs = serialize(ItemType.query.get(obj_id))
    if objs:
        return jsonify(objs[0])
    return "not found", 404


@app.route("/item_type", methods=['POST'])
def item_type_save():
    try:
        new_item_type = ItemType(**request.form)
        db.session.add(new_item_type)
        db.session.commit()
    except BaseException as error:
        return str(error), 400
    return "success", 200
