from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email

class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField('Email Address:', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Create Account')