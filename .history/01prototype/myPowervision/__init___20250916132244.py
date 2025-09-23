from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from myPowervision import routes, models
app = Flask(__name__)