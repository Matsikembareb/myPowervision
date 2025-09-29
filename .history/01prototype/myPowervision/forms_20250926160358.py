from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import sqlalchemy as sa
from myPowervision import db
from myPowervision.models import Permission, Staff, User, Role

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

class StaffForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    department = StringField('Department', validators=[Length(max=64)])
    position = StringField('Position', validators=[Length(max=64)])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        staff = db.session.scalar(sa.select(Staff).where(Staff.email == email.data))
        if staff is not None:
            raise ValidationError('Email already exists. Please use a different email address.')

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(min=2, max=64)])
    description = StringField('Description', validators=[Length(max=256)])
    submit = SubmitField('Submit')

    def validate_name(self, name):  # Changed from validate_role to validate_name
        role = db.session.scalar(sa.select(Role).where(Role.name == name.data))
        if role is not None:
            raise ValidationError('Role already exists.')  # Use ValidationError instead of ValueError
class PermissionForm(FlaskForm):
    name = StringField('Permission Name', validators=[DataRequired(), Length(min=2, max=64)])
    description = StringField('Description', validators=[Length(max=256)])
    submit = SubmitField('Submit')

    def validate_name(self, name):  # Changed from validate_role to validate_name
        permission = db.session.scalar(sa.select(Permission).where(Permission.name == name.data))
        if permission is not None:
            raise ValidationError('Permission already exists.')
