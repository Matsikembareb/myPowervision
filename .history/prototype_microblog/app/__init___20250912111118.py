from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
import os

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', True))