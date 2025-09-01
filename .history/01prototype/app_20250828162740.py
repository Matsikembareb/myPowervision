from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



@app.route("/")
def home_page():
    return render_template("base.html")

@app.route("/register")
def register_page():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)