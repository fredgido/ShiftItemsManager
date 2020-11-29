from flask import Flask, render_template
app = Flask(__name__)


# Routes
@app.route("/")
def index():
    return render_template('dashindex.html', item_type_list=[{"name": "Lanterna"}])


if __name__ == '__main__':
    app.run(debug=True)
