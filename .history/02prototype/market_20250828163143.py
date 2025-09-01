from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

import routes  # Import routes after app and db are defined
import models  # Import models after app and db are defined



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)