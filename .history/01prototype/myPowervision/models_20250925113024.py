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
    role: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='user')
    account_owner: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True)
    activity_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='offline')
    availability_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='available')
    created_at: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_seen: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_login: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    approval_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='pending')

    def __repr__(self):
        return '<User {}>'.format(self.username)

#Roles class
class Role(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    permissions: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'Role("{self.id}","{self.name}","{self.description}")'

#Permissions class
class Permission(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    permission: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

#Staff class
class Staff(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    staff_id: so.Mapped[int] = so.mapped_column(sa.String('staff.id'), index=True, unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    surname: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(15), unique=True, index=True)
    position: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    department: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    hire_date: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    salary: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    allowances_worth: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    deductions_worth: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    bank_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    bank_account_number: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True)
    bank_account_type: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    date_created: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_updated: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))

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