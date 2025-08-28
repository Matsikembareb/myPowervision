from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key='your_secret_key'

class item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
@app.route("/")
def home_page():
    return render_template("base.html")

@app.route("/register")
def register_page():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)