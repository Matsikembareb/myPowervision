from myPowervision import app
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlsplit
import sqlalchemy as sa

from myPowervision import db
from myPowervision.forms import DepartmentForm, LoginForm, PositionForm, RegistrationForm, RoleForm, PermissionForm, StaffForm, JobForm
from myPowervision.models import Department, Permission, Role, Staff, User, role_permission, Job, Position, Customer


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
        new_staff = Staff(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone=form.phone.data,
            department_id=form.department.data,
            position_id=form.position.data,
        )
        db.session.add(new_staff)
        db.session.commit()
        flash('Staff created successfully!', category='success')
        return redirect(url_for('staffManagement'))
    return render_template('staff_management/create_staff.html', title='Create Staff', active='staff', form=form)
# ---------------------------------Departments--------------------------------------
@app.route("/departments")
def departmentManagement():
    departments = db.session.scalars(sa.select(Department)).all()
    return render_template('staff_management/departments.html', title='Department Management', active='departments', departments=departments)
@app.route("/create-department", methods=['GET', 'POST'])
def create_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        new_department = Department(
            name=form.name.data,  # Changed from title to name
            description=form.description.data
        )
        db.session.add(new_department)
        db.session.commit()
        flash('Department created successfully!', category='success')
        return redirect(url_for('departmentManagement'))
    return render_template('staff_management/create_department.html', title='Create Department', active='department', form=form)
# ---------------------------------Positions--------------------------------------
@app.route("/positions")
def positionManagement():
    positions = db.session.scalars(sa.select(Position)).all()
    return render_template('staff_management/positions.html', title='Position Management', active='positions', positions=positions)

@app.route("/create-position", methods=['GET', 'POST'])
def create_position():
    form = PositionForm()
    if form.validate_on_submit():
        new_position = Position(
            name=form.name.data,  # Changed from title to name
            description=form.description.data
        )
        db.session.add(new_position)
        db.session.commit()
        flash('Position created successfully!', category='success')
        return redirect(url_for('positionManagement'))
    return render_template('staff_management/create_position.html', title='Create Position', active='position', form=form)

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
@app.route("/assign-permissions/<int:role_id>", methods=['GET', 'POST'])
def assign_permissions(role_id):
    role = db.session.scalar(sa.select(Role).where(Role.id == role_id))
    permissions = db.session.scalars(sa.select(Permission)).all()
    if not role:
        flash('Role not found!', 'danger')
        return redirect(url_for('roleManagement'))

    # Get currently assigned permission IDs
    assigned_permission_ids = db.session.scalars(
        sa.select(role_permission.c.permission_id).where(role_permission.c.role_id == role_id)
    ).all()


    return render_template('user_management/assign_permissions.html', 
                         title='Assign Permissions', 
                         active='assign permissions', 
                         role=role, 
                         permissions=permissions, 
                         assigned_permission_ids=assigned_permission_ids)

@app.route("/assign-permission/<int:role_id>/<int:permission_id>", methods=['GET', 'POST'])
def assign_permission(role_id, permission_id):
    try:
        # Check if the assignment already exists
        existing = db.session.scalar(
            sa.select(role_permission).where(
                sa.and_(
                    role_permission.c.role_id == role_id,
                    role_permission.c.permission_id == permission_id
                )
            )
        )
        
        if existing:
            flash('Permission already assigned to this role!', 'warning')
        else:
            # Insert new permission assignment
            db.session.execute(
                sa.insert(role_permission).values(
                    role_id=role_id,
                    permission_id=permission_id
                )
            )
            db.session.commit()
            flash('Permission assigned successfully!', 'success')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error assigning permission: {str(e)}', 'danger')
    
    return redirect(url_for('assign_permissions', role_id=role_id))

@app.route("/unassign-permission/<int:role_id>/<int:permission_id>", methods=['GET', 'POST'])
def unassign_permission(role_id, permission_id):
    try:
        # Delete the specific permission assignment
        result = db.session.execute(
            sa.delete(role_permission).where(
                sa.and_(
                    role_permission.c.role_id == role_id,
                    role_permission.c.permission_id == permission_id
                )
            )
        )
        
        if result.rowcount > 0:
            db.session.commit()
            flash('Permission unassigned successfully!', 'success')
        else:
            flash('Permission assignment not found!', 'warning')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error unassigning permission: {str(e)}', 'danger')
    
    return redirect(url_for('assign_permissions', role_id=role_id))
# ---------------------------------Permissions--------------------------------------
@app.route("/permissions")
def permissionManagement():
    permissions = db.session.scalars(sa.select(Permission)).all()
    return render_template('user_management/permissions.html', title='Permission Management', active='permissions', permissions=permissions)

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

#-----------------------------JOBS---------------------------------------------------
@app.route("/jobs")
def jobManagement():
    jobs = db.session.scalars(sa.select(Job)).all()
    return render_template('job_management/jobs.html', title='Job Management', active='jobs', jobs=jobs)

@app.route("/create-job", methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        new_job = Job(
            job_number=form.job_number.data,
            title=form.title.data,
            status='incomplete',  # or use form.status.data if you have a status field
            created_by_id=current_user.id        # Use ID, not username
            assigned_to_id=form.assigned_to.data, # This should be an ID from form
            customer_id=form.customer.data        # This should be an ID from form
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job created successfully!', category='success')
        return redirect(url_for('jobManagement'))
    return render_template('job_management/create_jobs.html', title='Create Job', active='jobs', form=form)

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

