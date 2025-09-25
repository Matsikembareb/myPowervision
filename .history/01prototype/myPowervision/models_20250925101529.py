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
    account_owner: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='self')
    activity_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='offline')
    availability_status: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), default='available')
    created_at: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_seen: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    last_login: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))



    def __repr__(self):
        return '<User {}>'.format(self.username)




#Staff class
class Staff(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(255), unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)

    def __repr__(self):
        return f'Admin("{self.id}","{self.email}","{self.username}")'
    
    