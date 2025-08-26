from flask import Flask, render_template, request
import json
import os
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# ======================================================================
# Firebase Setup
# ======================================================================
db = None
try:
    # Attempt to initialize Firebase with credentials from a local file
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully.")
except FileNotFoundError:
    print("Warning: 'credentials.json' not found. Firebase features will be disabled.")
    # Fallback to environment variable if the file is not found
    try:
        firebase_config_str = os.environ.get('__firebase_config')
        if firebase_config_str:
            firebase_config = json.loads(firebase_config_str)
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("Firebase initialized successfully from environment variable.")
        else:
            print("Warning: '__firebase_config' environment variable not found either.")
    except Exception as e:
        print(f"Error initializing Firebase from environment variable: {e}")
except Exception as e:
    print(f"An error occurred during Firebase initialization: {e}")




if __name__ == '__main__':
    app.run(debug=True)
