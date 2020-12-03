from flask import Flask, url_for, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db = SQLAlchemy(app)

if __name__ == '__main__':
    from views import *
    app.run(debug=True)
