from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from myPowervision import db, login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# Association table for many-to-many relationship between Role and Permission
role_permission = sa.Table(
    'role_permission',
    db.metadata,
    sa.Column('role_id', sa.Integer, sa.ForeignKey('role.id'), primary_key=True),
    sa.Column('permission_id', sa.Integer, sa.ForeignKey('permission.id'), primary_key=True)
)

#User class
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # Foreign key to Role
    role_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('role.id'), index=True)

    # Many-to-one relationship (many users can have one role)
    role: so.Mapped[Optional['Role']] = so.relationship(back_populates='users')

    # One-to-one relationship with Staff
    staff: so.Mapped[Optional['Staff']] = so.relationship(back_populates='user_account', uselist=False)

    # Job relationships with explicit foreign_keys
    created_jobs: so.WriteOnlyMapped['Job'] = so.relationship(
        foreign_keys='Job.created_by_id',
        back_populates='created_by'
    )
    assigned_jobs: so.WriteOnlyMapped['Job'] = so.relationship(
        foreign_keys='Job.assigned_to_id',
        back_populates='assigned_to'
    )
    
    # ADD THESE MISSING RELATIONSHIPS:
    stores_confirmations: so.WriteOnlyMapped['Job'] = so.relationship(
        foreign_keys='Job.stores_confirmation_by_id',
        back_populates='stores_confirmed_by'
    )
    
    work_completions: so.WriteOnlyMapped['Job'] = so.relationship(
        foreign_keys='Job.work_done_by_id',
        back_populates='work_done_by'
    )
    
    technical_approvals: so.WriteOnlyMapped['Job'] = so.relationship(
        foreign_keys='Job.technical_manager_approval_by_id',
        back_populates='technical_manager_approved_by'
    )
    
    payment_processings: so.WriteOnlyMapped['Job'] = so.relationship(
        foreign_keys='Job.accounts_payment_by_id',
        back_populates='accounts_paid_by'
    )
    
    activity_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='offline')
    availability_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='available')
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    last_login: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    approval_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='pending')

    def __repr__(self):
        return f'User({self.username})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_developer(self):
        """Check if user is a developer in IT Department"""
        if not self.staff:
            return False
        return (self.staff.department and self.staff.department.name == 'IT Department')
    
    def is_executive(self):
        """Check if user is in executive/management role"""
        if not self.staff:
            return False
        return (self.staff.department and self.staff.department.name == 'Executive')
    
    def is_logistics(self):
        """Check if user is in logistics/operations"""
        if not self.staff:
            return False
        return (self.staff.department and self.staff.department.name=='Logistics')
    
    def is_stores(self):
        """Check if user works in stores/inventory"""
        if not self.staff:
            return False
        return (self.staff.department and self.staff.department.name == 'Stores')
    
    def is_technical(self):
        """Check if user is in technical role"""
        if not self.staff:
            return False
        return (self.staff.department and self.staff.department.name == 'Engineering')
    
    def is_technical_manager(self):
        """Check if user is a technical manager"""
        if not self.staff:
            return False
        return (self.staff.position and self.staff.position.title == 'Technical Manager')
    
    def is_accounts(self):
        """Check if user is in accounts/finance role"""
        if not self.staff:
            return False
        return (self.staff.department and self.staff.department.name == 'Accounts')

    # ... rest of existing code ...
#Roles class
class Role(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # One-to-many relationship (one role can have many users)
    users: so.WriteOnlyMapped[User] = so.relationship(back_populates='role')
    
    # Many-to-many relationship with Permission
    permissions: so.Mapped[list['Permission']] = so.relationship(
        secondary=role_permission, 
        back_populates='roles'
    )

    def __repr__(self):
        return f'Role({self.id}, {self.name}, {self.description})'

#Permissions class
class Permission(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    permission: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    # Many-to-many relationship with Role
    roles: so.Mapped[list['Role']] = so.relationship(
        secondary=role_permission, 
        back_populates='permissions'
    )

    def __repr__(self):
        return f'Permission({self.id}, {self.permission}, {self.description})'

#Staff class
class Staff(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    staff_number: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    surname: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(15), unique=True, index=True)

    # Foreign keys
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), unique=True, index=True)
    department_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('department.id'), index=True)
    position_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('position.id'), index=True)

    hire_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    salary: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    allowances_worth: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    deductions_worth: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    bank_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    bank_account_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True)
    bank_account_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    date_created: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    last_updated: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))

    # Relationship mappings
    user_account: so.Mapped[Optional[User]] = so.relationship(back_populates='staff', uselist=False)

    # Many-to-one relationship with Department (many staff belong to one department)
    department: so.Mapped[Optional['Department']] = so.relationship(back_populates='staff_members')

    # Many-to-one relationship with Position (many staff can have same position)
    position: so.Mapped[Optional['Position']] = so.relationship(back_populates='staff_members')
    
    

    def __repr__(self):
        return f'Staff("{self.id}","{self.email}","{self.name}")'

#Department class
class Department(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # One-to-many relationship with Staff (one department has many staff)
    staff_members: so.WriteOnlyMapped['Staff'] = so.relationship(back_populates='department')

    def __repr__(self):
        return f'Department("{self.id}","{self.name}","{self.description}")'

#Position class
class Position(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # One-to-many relationship with Staff (one position can have many staff)
    staff_members: so.WriteOnlyMapped['Staff'] = so.relationship(back_populates='position')

    def __repr__(self):
        return f'Position("{self.id}","{self.title}","{self.description}")'

#Customer class
class Customer(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    contact_person: so.Mapped[str] = so.mapped_column(sa.String(64))
    customer_number: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    company_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True, index=True)
    phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(15), unique=True, index=True)
    address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    billing_address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(512))
    
    relationship_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='good')
    
    jobs: so.WriteOnlyMapped['Job'] = so.relationship(back_populates='customer')
    def __repr__(self):
        return f'Customer("{self.id}","{self.email}","{self.company_name}")'

# NEW: Vehicle class
class Vehicle(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    vehicle_number: so.Mapped[str] = so.mapped_column(sa.String(20), unique=True, index=True)
    make: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    model: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    year: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    color: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))
    vehicle_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))  # van, truck, car, etc.
    fuel_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32))  # petrol, diesel, electric
    capacity: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))  # passenger or cargo capacity
    status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), default='available')  # available, in_use, maintenance, retired
    mileage: so.Mapped[Optional[float]] = so.mapped_column(sa.Float)
    last_service_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime)
    next_service_date: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime)
    insurance_expiry: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(512))
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))

    # One-to-many relationship with Job
    jobs: so.WriteOnlyMapped['Job'] = so.relationship(back_populates='vehicle')

    def __repr__(self):
        return f'Vehicle("{self.vehicle_number}", "{self.make} {self.model}", "{self.status}")'

#Jobs class - UPDATED with new fields
class Job(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(512))
    status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='pending')
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    payment_terms: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    date_scheduled: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True)
    date_completed: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, index=True)
    notes: so.Mapped[Optional[str]] = so.mapped_column(sa.String(512))

    # NEW FIELDS
    time_allocated: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)  # Time in minutes
    job_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), unique=True, index=True)
    stores_confirmation: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=False, index=True)
    work_done: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=False, index=True)
    technical_manager_approval: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=False, index=True)
    accounts_payment: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=False, index=True)
    invoice_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), unique=True, index=True)

    # Foreign keys
    customer_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('customer.id'), index=True)
    assigned_to_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    created_by_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    vehicle_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('vehicle.id'), index=True)  
    stores_confirmation_by_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    work_done_by_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    technical_manager_approval_by_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), index=True)
    accounts_payment_by_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), index=True)

    # Additional relationships for the new foreign keys
    stores_confirmed_by: so.Mapped[Optional['User']] = so.relationship(
        foreign_keys=[stores_confirmation_by_id],
        back_populates='stores_confirmations'
    )
    
    work_done_by: so.Mapped[Optional['User']] = so.relationship(
        foreign_keys=[work_done_by_id],
        back_populates='work_completions'
    )
    
    technical_manager_approved_by: so.Mapped[Optional['User']] = so.relationship(
        foreign_keys=[technical_manager_approval_by_id],
        back_populates='technical_approvals'
    )
    
    accounts_paid_by: so.Mapped[Optional['User']] = so.relationship(
        foreign_keys=[accounts_payment_by_id],
        back_populates='payment_processings'
    )
    # Relationships - SPECIFY foreign_keys to avoid ambiguity
    customer: so.Mapped[Optional['Customer']] = so.relationship(back_populates='jobs')
    
    assigned_to: so.Mapped[Optional['User']] = so.relationship(
        foreign_keys=[assigned_to_id],  # Specify which FK to use
        back_populates='assigned_jobs'
    )
    
    created_by: so.Mapped[Optional['User']] = so.relationship(
        foreign_keys=[created_by_id],   # Specify which FK to use
        back_populates='created_jobs'
    )

    def __repr__(self):
        return f'Job("{self.id}","{self.title}","{self.status}")'
    
    def verified(self):
        """Check if all verifications are done"""
        return all([
            self.stores_confirmation,
            self.work_done,
            self.technical_manager_approval,
            self.accounts_payment
        ])

    def get_time_allocated_display(self):
        """Convert time allocated from minutes to human readable format"""
        if not self.time_allocated:
            return "Not specified"
        
        hours = self.time_allocated // 60
        minutes = self.time_allocated % 60
        
        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"