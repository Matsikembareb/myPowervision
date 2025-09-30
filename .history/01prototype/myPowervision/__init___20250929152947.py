import os
from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create Flask app
app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# Import models and routes at the bottom to avoid circular imports
from myPowervision import routes, models

# Add CLI command for initializing database with seed data
@app.cli.command()
def init_db():
    """Initialize database with default data."""
    import sqlalchemy as sa
    from myPowervision.models import Department, Position, Staff
    from datetime import datetime
    
    # Create tables
    db.create_all()
    
    # Create IT Department
    it_department = db.session.scalar(sa.select(Department).where(Department.name == 'IT Department'))
    if not it_department:
        it_department = Department(
            name='IT Department',
            description='Information Technology Department responsible for system development and maintenance'
        )
        db.session.add(it_department)
        db.session.flush()
        print("✓ Created IT Department")
    else:
        print("✓ IT Department already exists")
    
    # Create IT Attachee position
    it_attachee_position = db.session.scalar(sa.select(Position).where(Position.title == 'IT Attachee'))
    if not it_attachee_position:
        it_attachee_position = Position(
            title='IT Attachee',
            description='Junior IT position for software development and system support'
        )
        db.session.add(it_attachee_position)
        db.session.flush()
        print("✓ Created IT Attachee position")
    else:
        print("✓ IT Attachee position already exists")
    
    # Check if any staff exists
    staff_count = db.session.scalar(sa.select(sa.func.count(Staff.id)))
    if staff_count == 0:
        # Create default developer staff
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
        print("✓ Created default developer staff")
    else:
        print(f"✓ Staff already exists ({staff_count} records)")
    
    # Create additional departments
    departments_data = [
        ('Human Resources', 'Manages employee relations and recruitment'),
        ('Finance', 'Handles financial planning and accounting'),
        ('Operations', 'Manages day-to-day business operations'),
        ('Sales', 'Responsible for customer acquisition'),
    ]
    
    for dept_name, dept_desc in departments_data:
        existing_dept = db.session.scalar(sa.select(Department).where(Department.name == dept_name))
        if not existing_dept:
            new_dept = Department(name=dept_name, description=dept_desc)
            db.session.add(new_dept)
            print(f"✓ Created {dept_name} department")
    
    # Create additional positions
    positions_data = [
        ('Senior Developer', 'Senior software developer'),
        ('Project Manager', 'Manages projects and timelines'),
        ('System Administrator', 'Maintains IT infrastructure'),
        ('Business Analyst', 'Analyzes business requirements'),
    ]
    
    for pos_title, pos_desc in positions_data:
        existing_pos = db.session.scalar(sa.select(Position).where(Position.title == pos_title))
        if not existing_pos:
            new_pos = Position(title=pos_title, description=pos_desc)
            db.session.add(new_pos)
            print(f"✓ Created {pos_title} position")
    
    db.session.commit()
    print("\n🎉 Database initialization completed!")