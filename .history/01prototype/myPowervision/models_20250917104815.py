from myPowervision import db
#User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False, index=True, unique=True)
    lname = db.Column(db.String(255), nullable=False, index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    username = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(128))