from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
import sqlalchemy as sa
from myPowervision import db
from myPowervision.models import Department, Permission, Position, Staff, User, Role
from myPowervision.models import Job, Customer

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    staff_number = StringField('Staff ID', validators=[DataRequired(), Length(min=1, max=20)])
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
    staff_number = StringField('Staff Number', validators=[DataRequired(), Length(min=1, max=20)])
    name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=64)])
    surname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    department = SelectField('Department', coerce=int, validators=[DataRequired()])
    position = SelectField('Position', coerce=int, validators=[DataRequired()])
    
    hire_date = DateField('Hire Date', validators=[Optional()])
    salary = StringField('Salary', validators=[Optional(), Length(max=20)])
    allowances_worth = StringField('Allowances Worth', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        staff = db.session.scalar(sa.select(Staff).where(Staff.email == email.data))
        if staff is not None:
            raise ValidationError('Email already exists. Please use a different email address.')
    
    def validate_staff_number(self, staff_number):
        staff = db.session.scalar(sa.select(Staff).where(Staff.staff_number == staff_number.data))
        if staff is not None:
            raise ValidationError('Staff number already exists. Please use a different staff number.')

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        # Populate choices
        departments = db.session.scalars(sa.select(Department)).all()
        positions = db.session.scalars(sa.select(Position)).all()
        
        self.department.choices = [(0, 'Select Department')] + [(dept.id, dept.name) for dept in departments]
        
        # Check if Position has title or name field
        if positions:
            try:
                self.position.choices = [(0, 'Select Position')] + [(pos.id, pos.title) for pos in positions]
            except AttributeError:
                self.position.choices = [(0, 'Select Position')] + [(pos.id, pos.name) for pos in positions]
        else:
            self.position.choices = [(0, 'Select Position')]

class DepartmentForm(FlaskForm):
    # FIX: Change field name to match model
    name = StringField('Department Name', validators=[DataRequired(), Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Length(max=256)])
    submit = SubmitField('Submit')

    def validate_name(self, name):  # FIX: Change method name
        # FIX: Use 'name' instead of 'title'
        department = db.session.scalar(sa.select(Department).where(Department.name == name.data))
        if department is not None:
            raise ValidationError('Department already exists. Please use a different name.')

class PositionForm(FlaskForm):
    title = StringField('Position Title', validators=[DataRequired(), Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Length(max=256)])
    submit = SubmitField('Submit')

    def validate_title(self, title):
        position = db.session.scalar(sa.select(Position).where(Position.title == title.data))
        if position is not None:
            raise ValidationError('Position already exists. Please use a different title.')

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(min=2, max=64)])
    description = StringField('Description', validators=[Length(max=256)])
    submit = SubmitField('Submit')

    def validate_name(self, name):  # Changed from validate_role to validate_name
        role = db.session.scalar(sa.select(Role).where(Role.name == name.data))
        if role is not None:
            raise ValidationError('Role already exists.')  # Use ValidationError instead of ValueError
class PermissionForm(FlaskForm):
    permission = StringField('Permission Name', validators=[DataRequired(), Length(min=2, max=64)])
    description = StringField('Description', validators=[Length(max=256)])
    submit = SubmitField('Submit')

    def validate_permission(self, permission):  # Changed from validate_role to validate_permission
        permission = db.session.scalar(sa.select(Permission).where(Permission.permission == permission.data))
        if permission is not None:
            raise ValidationError('Permission already exists.')

class JobForm(FlaskForm):
    job_number = StringField('Job Number', validators=[DataRequired(), Length(min=1, max=20)])
    title = StringField('Job Title', validators=[DataRequired(), Length(min=1, max=128)])
    description = TextAreaField('Description', validators=[Length(max=512)])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    # These should be SelectFields with choices from database
    assigned_to = SelectField('Assigned To', coerce=int, validators=[DataRequired()])
    customer = SelectField('Customer', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Create Job')

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        # Populate choices from database
        self.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]
        self.customer.choices = [(customer.id, customer.contact_person) for customer in Customer.query.all()]

class CustomerForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=1, max=128)])
    contact_person = StringField('Contact Person', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    address = TextAreaField('Address', validators=[Length(max=256)])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        customer = db.session.scalar(sa.select(Customer).where(Customer.email == email.data))
        if customer is not None:
            raise ValidationError('Email already exists. Please use a different email address.')