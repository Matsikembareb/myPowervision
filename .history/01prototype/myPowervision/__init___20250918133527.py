from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
sess = Session(app)
from myPowervision import routes, models

with app.app_context():#to be deleted
    db.create_all()