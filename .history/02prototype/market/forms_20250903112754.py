from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    password1 = PasswordField('Password')
    password2 = PasswordField('Confirm Password')
    submit = SubmitField('Register')