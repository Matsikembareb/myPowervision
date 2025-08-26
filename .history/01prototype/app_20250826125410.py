from flask import Flask
app = Flask(__name__)

@app.route("/")
def home_page():
    return '<h1>Welcome to the home page!</h1>'


if __name__ == '__main__':
    app.run(debug=True)