import sqlalchemy as sa
import sqlalchemy.orm as so
from myPowervision import app, db
from myPowervision.models import User, Role, Permission, Staff, Department, Position

@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'Role': Role,
        'Permission': Permission,
        'Staff': Staff,
        'Department': Department,
        'Position': Position
    }