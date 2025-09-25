from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from myPowervision import db

#User class
class User(db.Model):
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
    
    activity_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='offline')
    availability_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='available')
    created_at: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_seen: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_login: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    approval_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='pending')

    def __repr__(self):
        return f'User({self.username})'

#Roles class
class Role(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    # One-to-many relationship (one role can have many users)
    users: so.WriteOnlyMapped[User] = so.relationship(back_populates='role')

    def __repr__(self):
        return f'Role({self.id}, {self.name}, {self.description})'

#Permissions class
class Permission(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    permission: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

#Staff class
class Staff(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    staff_number: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    surname: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(15), unique=True, index=True)
    position_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('position.id'), index=True)
    department_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('department.id'), index=True)
    
    # ADD THIS: Foreign key to User
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), unique=True, index=True)
    
    hire_date: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    salary: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    allowances_worth: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    deductions_worth: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    bank_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    bank_account_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True)
    bank_account_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    date_created: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_updated: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    
    # Relationship mapping
    user_account: so.Mapped[Optional[User]] = so.relationship(back_populates='staff', uselist=False)

    def __repr__(self):
        return f'Staff("{self.id}","{self.email}","{self.name}")'

#Department class
class Department(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'Department("{self.id}","{self.name}","{self.description}")'

#Position class
class Position(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'Position("{self.id}","{self.title}","{self.description}")'

#Customer class
class Customer(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True, index=True)

    def __repr__(self):
        return f'Customer("{self.id}","{self.email}","{self.name}")'