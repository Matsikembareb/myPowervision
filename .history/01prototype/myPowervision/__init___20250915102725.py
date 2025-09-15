from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from myPowervision import routes

if __name__ == '__main__':
    app.run(debug=True)