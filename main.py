from flask import Flask, url_for, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models.models import Item

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db = SQLAlchemy(app)


app = Flask(__name__)


# Routes
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/item", methods=['GET'])
def item_list():
    objs = Item.query.all()
    return jsonify([obj.__dict__ for obj in objs])


@app.route("/item", methods=['POST'])
def item_save():
    new_item = Item(**request.form.__dict__)


@app.route("/item_type")
def index():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
