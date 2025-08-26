from flask import Flask, render_template, request
import json
import os
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# ======================================================================
# Firebase Setup
# ======================================================================
# The Firebase configuration is provided by the canvas environment.
# We will check if it exists and initialize the app.
try:
    firebase_config_str = os.environ.get('__firebase_config')
    if firebase_config_str:
        firebase_config = json.loads(firebase_config_str)
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    else:
        print("Warning: '__firebase_config' not found. Firebase features will be disabled.")
except Exception as e:
    print(f"Error initializing Firebase: {e}")


# Get a reference to the Firestore database.
db = firestore.client()




if __name__ == '__main__':
    app.run(debug=True)
