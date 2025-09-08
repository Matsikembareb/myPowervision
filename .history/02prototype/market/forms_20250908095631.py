from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, EqualTo, DataRequired, Email
from market.models import User

class RegisterForm(FlaskForm):
    def validate(self, user_to_check):
        user = User.query.filter_by(username=user_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')
        
    username = StringField('Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField('Email Address:', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Create Account')