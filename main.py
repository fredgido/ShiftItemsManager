from flask import Flask, url_for, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db = SQLAlchemy(app)


# Routes
@app.route("/test")
def test():
    return render_template('dashindex.html', item_type_list=[{"name": "Test"}])

@app.route("/")
def index():
    return render_template('dashindex.html', item_type_list=[{"name": "Test"}])

@app.route("/item", methods=['GET'])
def item_list():
    objs = Item.query.all()
    return jsonify([obj.__dict__ for obj in objs])


@app.route("/item", methods=['POST'])
def item_save():
    new_item = db.Item(**request.form.__dict__)


@app.route("/item_type")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
