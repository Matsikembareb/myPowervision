from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.mapped_column[int] = so.mapped_column(primary_key=True)