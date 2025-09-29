from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from myPowervision import db, login

@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

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

    hire_date: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    salary: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    allowances_worth: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    deductions_worth: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    bank_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    bank_account_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True)
    bank_account_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    date_created: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_updated: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))

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
    email: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True, index=True)

    def __repr__(self):
        return f'Customer("{self.id}","{self.email}","{self.name}")'