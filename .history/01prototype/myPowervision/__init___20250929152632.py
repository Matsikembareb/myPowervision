from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login_page'

from myPowervision import routes, models

# Add this after db.init_app(app)
def create_default_records():
    """Create default records on app startup"""
    from myPowervision.models import Department, Position, Staff
    import sqlalchemy as sa
    from datetime import datetime
    
    with app.app_context():
        # Only run if no staff exists
        if db.session.scalar(sa.select(sa.func.count(Staff.id))) == 0:
            
            # Create IT Department
            it_department = Department(
                name='IT Department',
                description='Information Technology Department'
            )
            db.session.add(it_department)
            db.session.flush()
            
            # Create IT Attachee position
            it_attachee_position = Position(
                title='IT Attachee',
                description='Junior IT position'
            )
            db.session.add(it_attachee_position)
            db.session.flush()
            
            # Create developer staff
            developer_staff = Staff(
                staff_number='STF0001',
                name='System',
                surname='Developer',
                email='developer@powervision.com',
                phone='0700000000',
                department_id=it_department.id,
                position_id=it_attachee_position.id
            )
            db.session.add(developer_staff)
            db.session.commit()

# Call it on first request
@app.before_first_request
def initialize_database():
    db.create_all()
    create_default_records()