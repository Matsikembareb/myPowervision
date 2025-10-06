from myPowervision import app
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlsplit
import sqlalchemy as sa
from datetime import datetime, timezone

from myPowervision import db
from myPowervision.forms import DepartmentForm, LoginForm, PositionForm, RegistrationForm, RoleForm, PermissionForm, StaffForm, JobForm, CustomerForm
from myPowervision.models import Department, Permission, Role, Staff, User, role_permission, Job, Position, Customer


def create_default_data():
    """Create default data if database is empty"""
    # Check if any staff exists
    if db.session.scalar(sa.select(sa.func.count(Staff.id))) == 0:
        
        # Create default departments if they don't exist
        departments_data = [
            {'name': 'IT Department', 'description': 'Information Technology Department responsible for system development and maintenance'},
            {'name': 'Stores', 'description': 'Stores Department responsible for inventory management and storage'},
            {'name': 'Engineering', 'description': 'Engineering Department responsible for technical design and implementation'},
            {'name': 'Accounts', 'description': 'Accounts Department responsible for financial management and accounting'},
            {'name': 'Logistics', 'description': 'Logistics Department responsible for supply chain and transportation'},
            {'name': 'Executive', 'description': 'Executive Department responsible for strategic planning and management'}
        ]
        
        for dept_data in departments_data:
            existing_dept = db.session.scalar(sa.select(Department).where(Department.name == dept_data['name']))
            if not existing_dept:
                department = Department(
                    name=dept_data['name'],
                    description=dept_data['description']
                )
                db.session.add(department)
        
        db.session.flush()  # Flush to get department IDs
        
        # Create default positions if they don't exist
        positions_data = [
            {'title': 'IT Attachee', 'description': 'Junior IT position for software development and system support'},
            {'title': 'Storeman', 'description': 'Responsible for inventory management and warehouse operations'},
            {'title': 'Managing Director', 'description': 'Senior executive responsible for overall company management and strategic direction'},
            {'title': 'Technician', 'description': 'Technical specialist responsible for equipment maintenance and repair'},
            {'title': 'Technical Manager', 'description': 'Manager responsible for technical operations and team leadership'},
            {'title': 'Accountant', 'description': 'Financial specialist responsible for accounting and financial reporting'},
            {'title': 'Logistics Coordinator', 'description': 'Responsible for coordinating supply chain and transportation activities'}
        ]
        
        for pos_data in positions_data:
            existing_pos = db.session.scalar(sa.select(Position).where(Position.title == pos_data['title']))
            if not existing_pos:
                position = Position(
                    title=pos_data['title'],
                    description=pos_data['description']
                )
                db.session.add(position)
        
        db.session.flush()  # Flush to get position IDs
        
        # Get IT Department and IT Attachee position for staff creation
        it_department = db.session.scalar(sa.select(Department).where(Department.name == 'IT Department'))
        it_attachee_position = db.session.scalar(sa.select(Position).where(Position.title == 'IT Attachee'))
        
        # Create default developer staff
        developer_staff = Staff(
            staff_number='STF0001',
            name='System',
            surname='Developer',
            email='developer@powervision.com',
            phone='0700000000',
            department_id=it_department.id,
            position_id=it_attachee_position.id,

        )
        db.session.add(developer_staff)
        db.session.commit()
        
        print("Default departments, positions, and developer staff created!")

# Call this function in your home route
@app.route("/")
@app.route("/index")
def home_page():
    create_default_data()  # Add this line
    return render_template('index.html', title='Home', active='home')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if staff with the same staff number already exists
        existing_staff = db.session.scalar(sa.select(Staff).where(Staff.staff_number == form.staff_number.data))
        if existing_staff:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.flush()  # This assigns the ID to user without committing
            
            # Update the staff record with the user ID
            existing_staff.user_id = user.id
            db.session.commit()
            
            flash('Registration successful! You can now log in.', category='success')
            return redirect(url_for('login_page'))
        else:
            flash('Staff number does not exist!', category='danger')
            return render_template('auth/register.html', title='Register', active='register', form=form)
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
    staff = db.session.scalars(sa.select(Staff)).all()  # Add this line
    return render_template('staff_management/staff.html', title='Staff Management', active='staff', staff=staff)
@app.route("/create-staff", methods=['GET', 'POST'])
def create_staff():
    form = StaffForm()
    if form.validate_on_submit():
        new_staff = Staff(
            staff_number=form.staff_number.data,
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone=form.phone.data,
            department_id=form.department.data,  # This should work with SelectField
            position_id=form.position.data,      # This should work with SelectField
        )
        db.session.add(new_staff)
        db.session.commit()
        flash('Staff created successfully!', category='success')
        return redirect(url_for('staffManagement'))
    
    # Debug form errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    
    return render_template('staff_management/create_staff.html', title='Create Staff', active='staff', form=form)
@app.route("/edit-staff/<int:staff_id>", methods=['GET', 'POST'])
def edit_staff(staff_id):
    staff_member = db.session.scalar(sa.select(Staff).where(Staff.id == staff_id))
    if not staff_member:
        flash('Staff member not found!', 'danger')
        return redirect(url_for('staffManagement'))
    
    form = StaffForm(obj=staff_member)
    
    # Set current values for department and position
    if request.method == 'GET':
        form.department.data = staff_member.department_id
        form.position.data = staff_member.position_id
    
    if form.validate_on_submit():
        staff_member.staff_number = form.staff_number.data
        staff_member.name = form.name.data
        staff_member.surname = form.surname.data
        staff_member.email = form.email.data
        staff_member.phone = form.phone.data
        staff_member.department_id = form.department.data
        staff_member.position_id = form.position.data
        db.session.commit()
        flash('Staff updated successfully!', 'success')
        return redirect(url_for('staffManagement'))
    
    # FIX: Pass the staff object to the template
    return render_template('staff_management/edit_staff.html', title='Edit Staff', active='staff', form=form, staff=staff_member)

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
        new_position = Position(title=form.title.data, description=form.description.data)
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
        flash(f'Error revoking permission: {str(e)}', 'danger')
    
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
    return render_template('job_management/general/jobs.html', title='Job Management', active='jobs', jobs=jobs)
@app.route("/job/<int:job_id>")
def job_detail(job_id):
    job = db.session.scalar(sa.select(Job).where(Job.id == job_id))
    if not job:
        flash('Job not found!', category='danger')
        return redirect(url_for('jobManagement'))
    return render_template('job_management/general/job_detail.html', title='Job Detail', active='jobs', job=job)

@app.route("/all-scheduled-jobs", methods=['GET','POST'])
def all_scheduled_jobs():
    all_scheduled_jobs = db.session.scalars(sa.select(Job).where(Job.date_scheduled > datetime.now(timezone.utc))).all()
    return render_template('job_management/general/scheduled.html', title='My Jobs', active='jobs', jobs=all_scheduled_jobs)

@app.route("/all-pending-jobs", methods=['GET','POST'])
def all_pending_jobs():
    all_pending_jobs = db.session.scalars(sa.select(Job).where(Job.status.in_(['incomplete', '']), Job.date_scheduled <= datetime.now())).all()
    return render_template('job_management/general/pending.html', title='My Jobs', active='jobs', jobs=all_pending_jobs)

@app.route("/all-unverified-jobs", methods=['GET','POST'])
def all_unverified_jobs():
    all_unverified_jobs = db.session.scalars(sa.select(Job).where(Job.status.in_(['completed']))).all()
    return render_template('job_management/general/unverified.html', title='My Jobs', active='jobs', jobs=all_unverified_jobs)

@app.route("/all-closed-jobs", methods=['GET','POST'])
def all_closed_jobs():
    all_closed_jobs = db.session.scalars(sa.select(Job).where(Job.status == 'closed')).all()
    return render_template('job_management/general/closed.html', title='My Jobs', active='jobs', jobs=all_closed_jobs)

@app.route("/statistics")
def statistics():
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Calculate statistics
    total_jobs = db.session.scalar(sa.select(func.count(Job.id))) or 0
    
    # Count jobs by status
    completed_verified = db.session.scalar(
        sa.select(func.count(Job.id))
        .where(Job.status == 'completed')
        .where(Job.technical_manager_approval == True)
    ) or 0
    
    completed = db.session.scalar(
        sa.select(func.count(Job.id))
        .where(Job.status == 'completed')
    ) or 0
    
    scheduled = db.session.scalar(
        sa.select(func.count(Job.id))
        .where(Job.status == 'scheduled')
    ) or 0
    
    pending = db.session.scalar(
        sa.select(func.count(Job.id))
        .where(Job.status == 'pending')
    ) or 0
    
    # Calculate this week and month
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    jobs_this_week = db.session.scalar(
        sa.select(func.count(Job.id))
        .where(Job.created_at >= week_start)
    ) or 0
    
    jobs_this_month = db.session.scalar(
        sa.select(func.count(Job.id))
        .where(Job.created_at >= month_start)
    ) or 0
    
    # Get recent jobs
    recent_jobs = db.session.scalars(
        sa.select(Job)
        .order_by(Job.created_at.desc())
        .limit(10)
    ).all()
    
    # Create stats dictionary
    stats = {
        'total_jobs': total_jobs,
        'completed_verified': completed_verified,
        'completed': completed,
        'scheduled': scheduled,
        'pending': pending,
        'unverified': total_jobs - completed_verified,
        'jobs_this_week': jobs_this_week,
        'jobs_this_month': jobs_this_month
    }
    
    # Get weekly data for the last 4 weeks
    weekly_labels = []
    weekly_data = []
    
    for i in range(3, -1, -1):  # Last 4 weeks (3, 2, 1, 0 weeks ago)
        week_start = today - timedelta(weeks=i, days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Format week label
        if i == 0:
            weekly_labels.append('This Week')
        elif i == 1:
            weekly_labels.append('Last Week')
        else:
            weekly_labels.append(f'{i} Weeks Ago')
        
        # Count jobs for this week
        weekly_count = db.session.scalar(
            sa.select(func.count(Job.id))
            .where(Job.created_at >= week_start)
            .where(Job.created_at < week_end + timedelta(days=1))
        ) or 0
        
        weekly_data.append(weekly_count)
    
    # Get monthly data for the last 6 months
    monthly_labels = []
    monthly_data = []
    
    for i in range(5, -1, -1):  # Last 6 months
        if i == 0:
            month_start = today.replace(day=1)
            month_label = 'This Month'
        else:
            # Calculate previous months
            year = today.year
            month = today.month - i
            if month <= 0:
                month += 12
                year -= 1
            month_start = datetime(year, month, 1)
            month_label = month_start.strftime('%B %Y')
        
        # Calculate next month start for range
        if month_start.month == 12:
            next_month_start = month_start.replace(year=month_start.year + 1, month=1)
        else:
            next_month_start = month_start.replace(month=month_start.month + 1)
        
        monthly_labels.append(month_label)
        
        # Count jobs for this month
        monthly_count = db.session.scalar(
            sa.select(func.count(Job.id))
            .where(Job.created_at >= month_start)
            .where(Job.created_at < next_month_start)
        ) or 0
        
        monthly_data.append(monthly_count)

    
    return render_template(
        'job_management/general/stats.html',
        title='Statistics',
        active='statistics',
        stats=stats,
        recent_jobs=recent_jobs,
        weekly_labels=weekly_labels,
        weekly_data=weekly_data
    )

@app.route("/create-job", methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        new_job = Job(
            title=form.title.data,
            description=form.description.data,
            status='incomplete',
            created_by_id=current_user.id,
            assigned_to_id=form.assigned_to.data,
            customer_id=form.customer.data,
            date_scheduled=form.date_scheduled.data,
            payment_terms=form.payment_terms.data
        )
        db.session.add(new_job)
        db.session.commit()
        flash('Job created successfully!', category='success')
        return redirect(url_for('jobManagement'))
    return render_template('job_management/helpdesk/create_jobs.html', title='Create Job', active='jobs', form=form)
#---------------------------Logistics----------------------------------------
@app.route("/logistics-unverified")
def logisticsUnverified():
    jobs = db.session.scalars(sa.select(Job).where(Job.work_done != True)).all()
    return render_template('job_management/helpdesk/unverified_jobs.html', title='Logistics Unverified Jobs', active='jobs', jobs=jobs)

@app.route("/logistics-verified")
def logisticsVerified():
    jobs = db.session.scalars(sa.select(Job).where(Job.work_done == True)).all()
    return render_template('job_management/helpdesk/verified_jobs.html', title='Logistics Verified Jobs', active='jobs', jobs=jobs)

@app.route("/logistics-verify/<int:job_id>", methods=['GET', 'POST'])
def logistics_verify_job(job_id):
    job = db.session.scalar(sa.select(Job).where(Job.id == job_id))
    if not job:
        flash('Job not found!', category='danger')
        return redirect(url_for('jobManagement'))
    if request.method == 'POST':
        job_number_verify = request.form.get('job_number_verify', '')
        if job_number_verify == "":
            flash('Please enter a job number to verify.', category='danger')
            return redirect(url_for('logistics_verify_job', job_id=job.id))
        job.work_done_by_id = current_user.id
        job.job_number = job_number_verify
        job.work_done = True
        if job.verified():
            job.status = 'closed'
        db.session.commit()
        flash('Job verified successfully!', category='success')
        return redirect(url_for('logisticsUnverified'))
    return render_template('job_management/helpdesk/verify_job.html', title='Job Detail', active='jobs', job=job)

#-----------------------------------------Stores----------------------------------
@app.route("/stores-unverified")
def storesUnverified():
    jobs = db.session.scalars(sa.select(Job).where(Job.stores_confirmation != True)).all()
    return render_template('job_management/stores/unverified_jobs.html', title='Stores Unverified Jobs', active='jobs', jobs=jobs)

@app.route("/stores-verified")
def storesVerified():
    jobs = db.session.scalars(sa.select(Job).where(Job.stores_confirmation == True)).all()
    return render_template('job_management/stores/verified_jobs.html', title='Stores Verified Jobs', active='jobs', jobs=jobs)

@app.route("/stores-verify/<int:job_id>", methods=['GET', 'POST'])
def stores_verify_job(job_id):
    job = db.session.scalar(sa.select(Job).where(Job.id == job_id))
    if not job:
        flash('Job not found!', category='danger')
        return redirect(url_for('jobManagement'))
    if request.method == 'POST':
        job.stores_confirmation_by_id = current_user.id
        job.stores_confirmation = True
        if job.verified():
            job.status = 'closed'
        db.session.commit()
        flash('Materials for job verified successfully!', category='success')
        return redirect(url_for('storesUnverified'))
    return render_template('job_management/stores/verify_job.html', title='Job Detail', active='jobs', job=job)

#----------------------------------------------Accounts--------------------------------
@app.route("/accounts-unverified")
def accountsUnverified():
    jobs = db.session.scalars(sa.select(Job).where(Job.accounts_payment != True)).all()
    return render_template('job_management/accounts/unverified_jobs.html', title='Accounts Unverified Jobs', active='jobs', jobs=jobs)

@app.route("/accounts-verified")
def accountsClosed():
    jobs = db.session.scalars(sa.select(Job).where(Job.accounts_payment == True)).all()
    return render_template('job_management/accounts/verified_jobs.html', title='Accounts Verified Jobs', active='jobs', jobs=jobs)

@app.route("/accounts-close/<int:job_id>", methods=['GET', 'POST'])
def accounts_close_job(job_id):
    job = db.session.scalar(sa.select(Job).where(Job.id == job_id))
    if not job:
        flash('Job not found!', category='danger')
        return redirect(url_for('jobManagement'))
    if request.method == 'POST':
        invoice_number = request.form.get('invoice_number', '')
        if invoice_number == "":
            flash('Please enter an invoice number to verify.', category='danger')
            return redirect(url_for('accounts_close_job', job_id=job.id))
        job.accounts_payment_by_id = current_user.id
        job.invoice_number = invoice_number
        job.accounts_payment = True
        if job.verified():
            job.status = 'closed'
        db.session.commit()
        flash('Payment for job verified successfully!', category='success')
        return redirect(url_for('accountsUnverified'))
    return render_template('job_management/accounts/verify_job.html', title='Job Detail', active='jobs', job=job)
#----------------------------------------------Technical--------------------------------
@app.route("/technician-jobs")
def technician_jobs():
    jobs = db.session.scalars(sa.select(Job).where(Job.assigned_to_id == current_user.id)).all()
    return render_template('job_management/technician/assigned_jobs.html', title='My Jobs', active='jobs', jobs=jobs)

@app.route("/technician-update/<int:job_id>", methods=['GET', 'POST'])
def technician_update_job(job_id):
    job = db.session.scalar(sa.select(Job).where(Job.id == job_id))
    if not job:
        flash('Job not found!', category='danger')
        return redirect(url_for('jobManagement'))
    if request.method == 'POST':
        description = request.form.get('description', '')
        if description == "":
            flash('Please enter a description to verify.', category='danger')
            return redirect(url_for('technician_update_job', job_id=job.id))
        job.description = description
        job.notes = request.form.get('notes', '')
        db.session.commit()
        flash('Job updated successfully!', category='success')
        return redirect(url_for('technician_update_job', job_id=job.id))
    return render_template('job_management/technician/update_job.html', title='Job Detail', active='jobs', job=job)

@app.route("/complete-job/<int:job_id>", methods=['GET','POST'])
def complete_job(job_id):
    job = db.session.scalar(sa.select(Job).where(Job.id == job_id))
    if not job:
        flash('Job not found!', category='danger')
        return redirect(url_for('technician_update_job', job_id=job.id))
    job.status = 'completed'
    job.date_completed = datetime.now(timezone.utc)
    if job.verified():
            job.status = 'closed'
    db.session.commit()
    flash('Job marked as complete!', category='success')
    return redirect(url_for('technician_update_job', job_id=job.id))

@app.route("/scheduled-jobs", methods=['GET','POST'])
def scheduled_jobs():
    scheduled_jobs = db.session.scalars(sa.select(Job).where(Job.assigned_to_id == current_user.id, Job.date_scheduled > datetime.now(timezone.utc))).all()
    return render_template('job_management/technician/scheduled.html', title='My Jobs', active='jobs', jobs=scheduled_jobs)

@app.route("/pending-jobs", methods=['GET','POST'])
def pending_jobs():
    pending_jobs = db.session.scalars(sa.select(Job).where(Job.assigned_to_id == current_user.id, Job.status.in_(['incomplete', '']), Job.date_scheduled <= datetime.now())).all()
    return render_template('job_management/technician/pending.html', title='My Jobs', active='jobs', jobs=pending_jobs)

@app.route("/completed-jobs", methods=['GET','POST'])
def completed_jobs():
    completed_jobs = db.session.scalars(sa.select(Job).where(Job.assigned_to_id == current_user.id, Job.status.in_(['completed', 'closed']))).all()
    return render_template('job_management/technician/completed.html', title='My Jobs', active='jobs', jobs=completed_jobs)

#----------------------------------------------Technical Manager--------------------------------
@app.route("/tech-unverified")
def techUnverified():
    jobs = db.session.scalars(sa.select(Job).where(Job.technical_manager_approval != True)).all()
    return render_template('job_management/technical_manager/unverified_jobs.html', title='tech Unverified Jobs', active='jobs', jobs=jobs)

@app.route("/tech-verified")
def techVerified():
    jobs = db.session.scalars(sa.select(Job).where(Job.technical_manager_approval == True)).all()
    return render_template('job_management/technical_manager/verified_jobs.html', title='tech Verified Jobs', active='jobs', jobs=jobs)

@app.route("/tech-verify/<int:job_id>", methods=['GET', 'POST'])
def tech_verify_job(job_id):
    job = db.session.scalar(sa.select(Job).where(Job.id == job_id))
    if not job:
        flash('Job not found!', category='danger')
        return redirect(url_for('jobManagement'))
    if request.method == 'POST':
        job.technical_manager_approval_by_id = current_user.id
        job.technical_manager_approval = True
        if job.verified():
            job.status = 'closed'
        db.session.commit()
        flash('Job approved successfully!', category='success')
        return redirect(url_for('techUnverified'))
    return render_template('job_management/technical_manager/verify_job.html', title='Job Detail', active='jobs', job=job)

# ---------------------------------CUSTOMERS-----------------------------------------
@app.route("/customers")
def customerManagement():
    customers = db.session.scalars(sa.select(Customer)).all()
    return render_template('customer_management/customers.html', title='Customer Management', active='customers', customers=customers)

@app.route("/create-customer", methods=['GET', 'POST'])
def create_customer():
    form = CustomerForm()  # Create the form
    if form.validate_on_submit():
        new_customer = Customer(
            company_name=form.company_name.data,
            customer_number=form.customer_number.data,
            contact_person=form.contact_person.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            billing_address=form.billing_address.data,
            notes=form.notes.data
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer created successfully!', category='success')
        return redirect(url_for('customerManagement'))
    
    return render_template('customer_management/create_customer.html', title='Create Customer', active='customers', form=form)

@app.route("/edit-customer/<int:customer_id>", methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        flash('Customer not found!', category='danger')
        return redirect(url_for('customerManagement'))
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.company_name = form.company_name.data
        customer.customer_number = form.customer_number.data
        customer.contact_person = form.contact_person.data
        customer.email = form.email.data
        customer.phone = form.phone.data
        customer.address = form.address.data
        customer.billing_address = form.billing_address.data
        customer.notes = form.notes.data
        db.session.commit()
        flash('Customer updated successfully!', category='success')
        return redirect(url_for('customerManagement'))
    return render_template('customer_management/edit_customer.html', title='Edit Customer', active='customers', form=form)

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

