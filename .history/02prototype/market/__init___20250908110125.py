from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '6a602ce11149aca20dfd8dda'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from market import routes
from market.models import Item


