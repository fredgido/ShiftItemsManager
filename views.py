from flask import render_template, jsonify, request, session, url_for, redirect, g

from main import app, db
from models import Item, ItemType, Reservation
from utils import serialize


@app.route("/test")
def test():
    all_item_type = [{"item_name": "Radio"}, {"item_name": "Baterias"}, {"item_name": "Chaves"}]
    return render_template('dashindex.html', item_type_list=all_item_type)

# Login test with dummy data
users = {}
users["Rui"] = {id: 1, 'username': 'Rui', 'password': 'teste', 'permission': 'superuser'}

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form.get('sp_uname')
        password = request.form.get('sp_pass')

        if users.get(username).get(password) == password:
            session['username'] = username
            session['password'] = password
            return redirect(url_for("index"))
        else:
            return "Fail"
        
    return "Login Page"

# End Login

@app.before_request
def before_request():
    username = session.get('username')
    password = session.get('password')

    if users.get(username) and users.get(username).get(password) == password:
        g.user = users.get(username)
    else:
        g.user = {}

@app.route("/")
def index():
    all_item_type = ItemType.query.all()

    print(g.user)

    return render_template('dashindex.html', item_type_list=all_item_type, user=g.user)


@app.route("/display/<item_type>")
def display(item_type):
    all_item_type = ItemType.query.all()
    item_type_selected = ItemType.query.filter_by(item_name=item_type).all()
    if len(item_type_selected) >  0:
        item_type_selected = item_type_selected[0]
    else:
        item_type_selected = ItemType.query.all()[0]
    item_list = Item.query.filter_by(item_type_id=item_type_selected.id).all()
    return render_template(
        'dashindex.html',
        item_type_list=all_item_type,
        item_type_selected=item_type_selected,
        item_display_list=item_list,
        disp=display,
    )


@app.route("/reservation/<item_type>")
def reservation(item_type):
    all_item_type = ItemType.query.all()
    item_type_selected = ItemType.query.filter_by(item_name=item_type).all()
    if len(item_type_selected)> 0:
        item_type_selected = item_type_selected[0]
    else:
        item_type_selected = ItemType.query.all()[0]
    reservation_list = Reservation.query.join(Item).filter_by(item_type_id=item_type_selected.id).all()
    return render_template(
        'dashindex.html',
        item_type_list=all_item_type,
        item_type_selected=item_type_selected,
        reservation_list=reservation_list,
        )


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
