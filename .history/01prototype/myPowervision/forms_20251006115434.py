from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from wtforms.widgets import DateTimeLocalInput, CheckboxInput, ListWidget
import sqlalchemy as sa
from myPowervision import db
from myPowervision.models import Department, Permission, Position, Staff, User, Role
from myPowervision.models import Job, Customer
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField, DateTimeField, DateTimeLocalField
from myPowervision.models import Vehicle
from wtforms import IntegerField
from wtforms.widgets import NumberInput
from wtforms import SelectMultipleField

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

    def __init__(self, staff_id=None, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.staff_id = staff_id
        # Populate choices
        departments = db.session.scalars(sa.select(Department)).all()
        positions = db.session.scalars(sa.select(Position)).all()
        
        self.department.choices = [(0, 'Select Department')] + [(dept.id, dept.name) for dept in departments]
        self.position.choices = [(0, 'Select Position')] + [(pos.id, pos.title) for pos in positions]

    def validate_email(self, email):
        staff = db.session.scalar(sa.select(Staff).where(Staff.email == email.data))
        if staff is not None and (self.staff_id is None or staff.id != self.staff_id):
            raise ValidationError('Email already exists. Please use a different email address.')
    
    def validate_staff_number(self, staff_number):
        staff = db.session.scalar(sa.select(Staff).where(Staff.staff_number == staff_number.data))
        if staff is not None and (self.staff_id is None or staff.id != self.staff_id):
            raise ValidationError('Staff number already exists. Please use a different staff number.')

class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired(), Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=256)])
    submit = SubmitField('Submit')

    def validate_name(self, name):  # FIX: Change method name
        # FIX: Use 'name' instead of 'title'
        department = db.session.scalar(sa.select(Department).where(Department.name == name.data))
        if department is not None:
            raise ValidationError('Department already exists. Please use a different name.')

class PositionForm(FlaskForm):
    title = StringField('Position Title', validators=[DataRequired(), Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=256)])
    submit = SubmitField('Submit')

    def validate_title(self, title):
        position = db.session.scalar(sa.select(Position).where(Position.title == title.data))
        if position is not None:
            raise ValidationError('Position already exists. Please use a different title.')

class RoleForm(FlaskForm):
    name = StringField('Role Name', validators=[DataRequired(), Length(min=2, max=64)])
    description = StringField('Description', validators=[Optional(), Length(max=256)])
    submit = SubmitField('Submit')

    def validate_name(self, name):  # Changed from validate_role to validate_name
        role = db.session.scalar(sa.select(Role).where(Role.name == name.data))
        if role is not None:
            raise ValidationError('Role already exists.')

class PermissionForm(FlaskForm):
    permission = StringField('Permission Name', validators=[DataRequired(), Length(min=2, max=64)])
    description = StringField('Description', validators=[Optional(), Length(max=256)])
    submit = SubmitField('Submit')

    def validate_permission(self, permission):  # Changed from validate_role to validate_permission
        permission = db.session.scalar(sa.select(Permission).where(Permission.permission == permission.data))
        if permission is not None:
            raise ValidationError('Permission already exists.')

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
    
    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class JobForm(FlaskForm):
    job_number = StringField('Job Number', validators=[Optional(), Length(min=1, max=20)])
    invoice_number = StringField('Invoice Number', validators=[Optional(), Length(min=1, max=20)])
    created_at = DateTimeLocalField('Created Date', validators=[Optional()])
    date_scheduled = DateTimeLocalField('Scheduled Date & Time', validators=[Optional()])
    title = StringField('Job Title', validators=[DataRequired(), Length(min=1, max=128)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=512)])
    
    # Use your custom TimeField instead of IntegerField
    time_allocated_hours = IntegerField('Hours', validators=[Optional()], widget=NumberInput(min=0, max=23), default=0)
    time_allocated_minutes = IntegerField('Minutes', validators=[Optional()], widget=NumberInput(min=0, max=59), default=0)
    
    assigned_to = SelectField('Assigned To', coerce=int, validators=[DataRequired()])
    customer = SelectField('Customer', coerce=int, validators=[DataRequired()])
    vehicle = SelectField('Vehicle', coerce=int, validators=[Optional()])
    
    # Use MultiCheckboxField for better UX
    assistants = MultiCheckboxField('Assistants', coerce=int, validators=[Optional()])
    
    contact_person = StringField('Contact Person', validators=[Optional(), Length(min=1, max=64)])
    contact_phone = StringField('Contact Phone', validators=[Optional(), Length(max=20)])
    contact_email = StringField('Contact Email', validators=[Optional(), Email(), Length(max=64)])
    payment_terms = StringField('Payment Terms', validators=[Optional(), Length(max=128)])
    submit = SubmitField('Create Job')
    
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        # Populate choices from database
        users = db.session.scalars(sa.select(User)).all()
        customers = db.session.scalars(sa.select(Customer)).all()
        vehicles = db.session.scalars(sa.select(Vehicle)).all()
        
        self.assigned_to.choices = [(0, 'Select User')] + [(user.id, user.username) for user in users]
        self.customer.choices = [(0, 'Select Customer')] + [(customer.id, customer.contact_person) for customer in customers]
        self.vehicle.choices = [(0, 'Select Vehicle')] + [(vehicle.id, f"{vehicle.vehicle_number} - {vehicle.make} {vehicle.model}") for vehicle in vehicles]
        
        # Populate assistants choices (exclude the assigned user if needed)
        self.assistants.choices = [(user.id, user.username) for user in users]

class CustomerForm(FlaskForm):
    customer_number = StringField('Customer ID', validators=[DataRequired(), Length(min=1, max=20)])
    company_name = StringField('Company Name', validators=[Optional(), Length(max=128)])
    contact_person = StringField('Contact Person', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=256)])
    billing_address = TextAreaField('Billing Address', validators=[Optional(), Length(max=256)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=512)])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        customer = db.session.scalar(sa.select(Customer).where(Customer.email == email.data))
        if customer is not None:
            raise ValidationError('Email already exists. Please use a different email address.')

class VehicleForm(FlaskForm):
    vehicle_number = StringField('License Plate', validators=[DataRequired(), Length(min=1, max=20)])
    make = StringField('Make', validators=[Optional(), Length(max=64)])
    model = StringField('Model', validators=[Optional(), Length(max=64)])
    year = StringField('Year', validators=[Optional(), Length(max=4)])
    color = StringField('Color', validators=[Optional(), Length(max=32)])
    vehicle_type = SelectField('Vehicle Type', choices=[
        ('', 'Select Type'),
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('motorcycle', 'Motorcycle'),
        ('other', 'Other')
    ], validators=[Optional()])
    fuel_type = SelectField('Fuel Type', choices=[
        ('', 'Select Fuel Type'),
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('other', 'Other')
    ], validators=[Optional()])
    capacity = StringField('Capacity', validators=[Optional(), Length(max=64)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=512)])
    submit = SubmitField('Submit')

    def __init__(self, vehicle_id=None, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.vehicle_id = vehicle_id

    def validate_vehicle_number(self, vehicle_number):
        vehicle = db.session.scalar(sa.select(Vehicle).where(Vehicle.vehicle_number == vehicle_number.data))
        if vehicle is not None and (self.vehicle_id is None or vehicle.id != self.vehicle_id):
            raise ValidationError('Vehicle number already exists. Please use a different vehicle number.')