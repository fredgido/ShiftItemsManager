from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "SECRET_TESTING"

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

db = SQLAlchemy(app)

if __name__ == '__main__':
    from views import *
    app.run(debug=True)
