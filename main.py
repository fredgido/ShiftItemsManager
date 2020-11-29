from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

db = SQLAlchemy(app)

# Routes
@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
