import hashlib

from flask import render_template, jsonify, request, session, url_for, redirect, g, flash, abort
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import is_safe_url
from flask_login import login_user, current_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from main import app, db, login_manager
from models import Item, ItemType, Reservation, User
from utils import serialize

admin = Admin(app, name='microblog', template_mode='bootstrap3')


class UserModelAdmin(ModelView):
    def on_model_change(self, form, instance,x,y=None):
        if "sha" not in instance.password:
            instance.set_password(instance.password)


admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(ItemType, db.session))
admin.add_view(ModelView(Reservation, db.session))
admin.add_view(UserModelAdmin(User, db.session))


@app.route("/test")
def test():
    all_item_type = [{"item_name": "Radio"}, {"item_name": "Baterias"}, {"item_name": "Chaves"}]
    return render_template('dashindex.html', item_type_list=all_item_type)


# Login test with dummy data
users = {
    "Rui": {id: 1, 'username': 'Rui', 'password': '46070d4bf934fb0d4b06d9e2c46e346944e322444900a435d7d9a95e6d7435f5',
            'permission': 'superuser'}
}


# Form model - Flask-WTF
class LoginForm(FlaskForm):
    sp_uname = StringField('Username', validators=[DataRequired()])
    sp_pass = PasswordField('Password', validators=[DataRequired()])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = None #User()

    # Se o utilizador já se encontrar autenticado
    if current_user.is_authenticated:
        redirect(url_for('index'))

    # Verifica se o formulário foi submetido através de POST
    if form.validate_on_submit():
        # session.pop('user_id', None)

        username = request.form.get('sp_uname')
        password = request.form.get('sp_pass')

        # Verificar se o nome de utilizador se encontra registado na nossa BD
        check_user = User.query.filter_by(username=username).first()

        # Cifrar password para comparar com a password cifrada na nossa DB
        # hashpw = hashlib.sha256()
        # hashpw.update(password.encode())

        if check_user and check_user.check_password(password):
            login_user(check_user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Credenciais incorretas. Por favor tente novamente.')
        return redirect(url_for('index'))

        # if users.get(username) and users.get(username).get('password') == hashpw.hexdigest():
        #    session['username'] = username
        #    session['password'] = hashpw.hexdigest()
        #    return redirect(url_for("index", login="Logged in"))
        # else:
        #    flash("Username ou password incorreto. Por favor tente outra vez.", "error")
        #    return redirect(url_for("index"))

    return "Login Page"


# End Login

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.before_request
def before_request():
    username = session.get('username')
    password = session.get('password')

    if password:
        if users.get(username) and users.get(username).get('password') == password:
            g.user = users.get(username)
        else:
            g.user = {}
    else:
        g.user = {}


@app.route("/")
def index():
    return redirect(url_for("display", item_type=ItemType.query.all()[0].item_name))


@app.route("/display/")
def display_index():
    return redirect(url_for("display", item_type=ItemType.query.all()[0].item_name))


@app.route("/display/<item_type>")
def display(item_type):
    loginForm = LoginForm()

    all_item_type = ItemType.query.all()
    item_type_selected = ItemType.query.filter_by(item_name=item_type).all()
    if len(item_type_selected) > 0:
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
        form=loginForm,
    )


@app.route("/reservation/")
def reservation_index():
    return redirect(url_for("reservation", item_type=ItemType.query.all()[0].item_name))


@app.route("/reservation/<item_type>")
def reservation(item_type):
    login_form = LoginForm()
    all_item_type = ItemType.query.all()
    item_type_selected = ItemType.query.filter_by(item_name=item_type).all()
    if len(item_type_selected) > 0:
        item_type_selected = item_type_selected[0]
    else:
        item_type_selected = ItemType.query.all()[0]
    reservation_list = Reservation.query.join(Item).filter_by(item_type_id=item_type_selected.id).all()
    return render_template('dashindex.html', item_type_list=all_item_type, item_type_selected=item_type_selected,
                           reservation_list=reservation_list, login=login_form)


@app.route("/reservation/personal")
def personal_reservation():
    login_form = LoginForm()
    all_item_type = ItemType.query.all()
    item_type_selected = ItemType.query.all()
    if len(item_type_selected) > 0:
        item_type_selected = item_type_selected[0]
    else:
        item_type_selected = ItemType.query.all()[0]
    reservation_list = Reservation.query.filter_by(user_id=current_user.id).join(Item).filter_by(item_type_id=item_type_selected.id).all()
    return render_template('dashindex.html', item_type_list=all_item_type, item_type_selected=item_type_selected,
                           reservation_list=reservation_list, login=login_form)

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
