from myPowervision import app
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlsplit
import sqlalchemy as sa

from myPowervision import db
from myPowervision.forms import LoginForm, RegistrationForm, RoleForm, PermissionForm, StaffForm
from myPowervision.models import Permission, Role, Staff, User, role_permission


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html', title='Home', active='home')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', category='success')
        return redirect(url_for('login_page'))
    return render_template('auth/register.html', title='Register', active='register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or urlsplit(next_page).netloc != '':
                    next_page = url_for('home_page')
                flash(f'Login successful for user {form.username.data}', category='success')
                return redirect(next_page)
            else:
                flash('Invalid password!', category='danger')
                return redirect(url_for('login_page'))
        else:
            flash('User not found!', category='danger')
            return redirect(url_for('login_page'))

    return render_template('auth/login.html', title='Sign In', active='login', form=form)

@app.route('/forgot-password')
def forgot_password_page():
    return render_template('auth/forgot_password.html', title='Forgot Password', active='forgot_password')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('home_page'))

# ---------------------------------STAFF, DEPARTMENTS, POSITIONS--------------------------------------
# ---------------------------------Staff--------------------------------------
@app.route("/staff")
def staffManagement():
    return render_template('staff_management/staff.html', title='Staff Management', active='staff')
@app.route("/create-staff", methods=['GET', 'POST'])
def create_staff():
    form = StaffForm()
    if form.validate_on_submit():
        new_staff = Staff(name=form.name.data, department=form.department.data, position=form.position.data)
        db.session.add(new_staff)
        db.session.commit()
        flash('Staff created successfully!', category='success')
        return redirect(url_for('staffManagement'))
    return render_template('staff_management/create_staff.html', title='Create Staff', active='staff', form=form)
# ---------------------------------Departments--------------------------------------
@app.route("/departments")
def departmentManagement():
    return render_template('staff_management/departments.html', title='Department Management', active='departments')
# ---------------------------------Positions--------------------------------------
@app.route("/positions")
def positionManagement():
    return render_template('staff_management/positions.html', title='Position Management', active='positions')

# ---------------------------------USERS, ROLES, PERMISSIONS--------------------------------------
# ---------------------------------Users--------------------------------------
@app.route("/users")
def userManagement():
    users = db.session.scalars(sa.select(User)).all()
    return render_template('user_management/users.html', title='User Management', active='users', users=users)

# ---------------------------------Roles--------------------------------------
@app.route("/roles")
def roleManagement():
    roles = db.session.scalars(sa.select(Role)).all()
    return render_template('user_management/roles.html', title='Role Management', active='roles', roles=roles)

@app.route("/create-role", methods=['GET', 'POST'])
def create_role():
    form = RoleForm()
    if form.validate_on_submit():
        new_role = Role(name=form.name.data, description=form.description.data)
        db.session.add(new_role)
        db.session.commit()
        flash('Role created successfully!', category='success')
        return redirect(url_for('roleManagement'))
    return render_template('user_management/create_role.html', title='Create Role', active='roles', form=form)

# ---------------------------------Permissions for Roles--------------------------------------
@app.route("/assign-permissions")


# ---------------------------------Permissions--------------------------------------
@app.route("/permissions")
def permissionManagement():
    permissions = db.session.scalars(sa.select(Permission)).all()
    roles = db.session.scalars(sa.select(Role)).all()
    rolepermissions = db.session.scalars(sa.select(role_permission)).all()
    return render_template('user_management/permissions.html', title='Permission Management', active='permissions', permissions=permissions, roles=roles, role_permissions=rolepermissions)

@app.route("/create-permission", methods=['GET', 'POST'])
def create_permission():
    form = PermissionForm()
    if form.validate_on_submit():
        new_permission = Permission(permission=form.permission.data, description=form.description.data)
        db.session.add(new_permission)
        db.session.commit()
        flash('Permission created successfully!', category='success')
        return redirect(url_for('permissionManagement'))
    return render_template('user_management/create_permission.html', title='Create Permission', active='permissions', form=form)
# ---------------------------------admin area--------------------------------------


# admin dashboard
@app.route("/admin/dashboard", methods=['GET','POST'])
def adminDashboard():
    if not session.get('admin_id'):
        return redirect(url_for('adminIndex'))
    total_users = User.query.count()
    approved_users = User.query.filter_by(status=1).count()
    disapproved_users = User.query.filter_by(status=0).count()
    return render_template("auth/admin/dashboard.html", title="Admin Dashboard", total_users=total_users, approved_users=approved_users, disapproved_users=disapproved_users)

# ADMIN get all users
@app.route("/admin/users", methods=['GET','POST'])
def adminUsers():
    if not session.get('admin_id'):
        return redirect(url_for('adminIndex'))
    users = User.query.all()
    if request.method == 'POST':
        # Fetch all users
        search = request.form.get('search')
        users = User.query.filter((User.fname.contains(search)) | (User.lname.contains(search)) | (User.email.contains(search))).all()
    return render_template("auth/admin/users.html", title="All Users", users=users)

# ADMIN approve user
@app.route("/admin/approve/<int:user_id>")
def adminApproveUser(user_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminIndex'))
    user = User.query.get(user_id)
    if user:
        user.status = 1  # Approve the user
        db.session.commit()
        flash("User approved successfully", "success")
    else:
        flash("Error!", "danger")
    return redirect(url_for('adminUsers'))

# ADMIN disapprove user
@app.route("/admin/disapprove")
def adminDisapproveUser(user_id):
    if not session.get('admin_id'):
        return redirect(url_for('adminIndex'))
    user = User.query.get(user_id)
    if user:
        user.status = 0  # Disapprove the user
        db.session.commit()
        flash("User disapproved successfully", "success")
    else:
        flash("Error!", "danger")
    return redirect(url_for('adminUsers'))
