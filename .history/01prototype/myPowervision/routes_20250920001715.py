from myPowervision import app
from flask import render_template, url_for, redirect, flash, session, request
from myPowervision.forms import LoginForm
from myPowervision import bcrypt
from myPowervision.models import User, Admin
from myPowervision import db

@app.route("/")
@app.route('/home')
def home_page():
    return render_template("index.html", title="Home", active="home")

@app.route("/register")
def register_page():
    return render_template("auth/register.html", title="Register", active="register")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for("home_page"))
    return render_template("auth/login.html", title="Login", active="login", form=form)

@app.route("/forgot-password")
def forgot_password_page():
    return render_template("auth/forgot_password.html", title="Forgot Password", active="forgot_password")




# main index
@app.route("/UMS")
def index():
    return render_template("auth/index.html")

# admin login
@app.route("/admin", methods=['GET','POST'])
def adminIndex():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if email == '' or username == '' or password == '':
            flash("Please fill all the fields", "danger")
            return redirect(url_for('adminIndex'))
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and bcrypt.check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            session['admin_name'] = admin.username
            flash("Login Success", "success")
            return redirect(url_for('adminDashboard'))
        else:
            flash("Invalid credentials. Please check all the fields", "danger")
            return redirect(url_for('adminIndex'))
    return render_template("auth/admin/index.html", title="Admin Login")

# admin dashboard
@app.route("/admin/dashboard", methods=['GET','POST'])
def adminDashboard():
    return render_template("auth/admin/dashboard.html", title="Admin Dashboard")

@app.route("/admin/logout")
def adminLogout():
    if not session.get('admin_id'):
        return redirect(url_for(adminIndex))
    if session.get('admin_id'):
        session.pop('user_id', None)
        session.pop('username', None)
        return redirect(url_for(index))

@app.route("/admin/dashboard", methods=['GET','POST'])
def adminApprove():
    return render_template("auth/admin/dashboard.html", title="Admin Dashboard")
@app.route("/admin/dashboard", methods=['GET','POST'])
def adminChangePassword():
    return render_template("auth/admin/dashboard.html", title="Admin Dashboard")


# ---------------------------------user area--------------------------------------

# user login
@app.route("/user", methods=['GET', 'POST'])
def userIndex():
    if session.get('user_id'):
        return redirect(url_for('userDashboard'))
    if request.method == 'POST':
        # process the form data
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if email == '' or username == '' or password == '':
            flash("Please fill all the fields", "danger")
            return redirect(url_for('userSignup'))
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Fix the status logic - 0 means not approved, 1 means approved
            if user.status == 1:
                flash("Your account is not approved by admin yet.", "warning")
                return redirect(url_for('userIndex'))
            else:
                session['user_id'] = user.id
                session['username'] = user.username
                flash("Login Success", "success")
                return redirect(url_for('userDashboard'))
        else:
            flash("Invalid credentials. Please check all the fields", "danger")
            return redirect(url_for('userIndex'))
    return render_template("auth/user/index.html", title="User Login")

# user registration
@app.route("/user/signup", methods=['GET', 'POST'])
def userSignup():
    if session.get('user_id'):
        return redirect(url_for('userDashboard'))
    if request.method == 'POST':
        print("Form submitted!")  # Debug print
        # process the form data
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        username = request.form.get('username')
        edu = request.form.get('edu')
        password = request.form.get('password')

        if fname == '' or lname == '' or email == '' or username == '' or edu == '' or password == '':
            flash("Please fill all the fields", "danger")
            return redirect(url_for('userSignup'))
        else:
            is_email = User.query.filter_by(email=email).first()
            if is_email:
                flash("Email already registered", "danger")
                return redirect(url_for('userSignup'))
            else:
                hashed_password = bcrypt.generate_password_hash(password, 10)
                user = User(fname=fname, lname=lname, email=email, username=username, edu=edu, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash("User registered successfully. Please wait for admin approval.", "success")
                return redirect(url_for('userIndex'))
    return render_template("auth/user/signup.html", title="User Signup")

#user dashboard
@app.route("/user/dashboard")
def userDashboard():
    if not session.get('user_id'):
        return redirect(url_for('userIndex'))
    id = session.get('user_id')
    user = User.query.filter_by(id=id).first()
    return render_template("auth/user/dashboard.html", title="User Dashboard", user=user)

#user logout
@app.route("/user/logout")
def userLogout():
    if not session.get('user_id'):
        return redirect(url_for('userIndex'))
    # Properly clear session
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been logged out successfully", "success")
    return redirect(url_for('userIndex'))

# user change Password
@app.route("/user/change-password", methods=['GET', 'POST'])
def userChangePassword():
    if not session.get('user_id'):
        return redirect(url_for('userIndex'))
    if request.method == 'POST':
        # process the form data
        email = request.form.get('email')
        password = request.form.get('password')

        if email == '' or password == '':
            flash("Please fill all the fields", "danger")
            return redirect(url_for('userChangePassword'))
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                hashed_password = bcrypt.generate_password_hash(password, 10)
                # Fix: Update the user object directly
                user.password = hashed_password
                db.session.commit()
                flash("Password changed successfully.", "success")
                return redirect(url_for('userIndex'))
            else:
                flash("User not found", "danger")
                return redirect(url_for('userChangePassword'))
    return render_template("auth/user/change_password.html", title="Change Password")

#user update profile
@app.route("/user/update-profile", methods=['GET', 'POST'])
def userUpdateProfile():
    if not session.get('user_id'):
        return redirect(url_for('userIndex'))
    
    user = User.query.filter_by(id=session.get('user_id')).first()
    
    if request.method == 'POST':
        # process the form data
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        username = request.form.get('username')
        edu = request.form.get('edu')

        if fname == '' or lname == '' or email == '' or username == '' or edu == '':
            flash("Please fill all the fields", "danger")
            return redirect(url_for('userUpdateProfile'))
        else:
            is_email = User.query.filter_by(email=email).first()
            if is_email and is_email.id != user.id:
                flash("Email already registered", "danger")
                return redirect(url_for('userUpdateProfile'))
            else:
                # Fix: Update the user object directly
                user.fname = fname
                user.lname = lname
                user.email = email
                user.username = username
                user.edu = edu
                db.session.commit()
                session['username'] = username
                flash("Profile updated successfully.", "success")
                return redirect(url_for('userDashboard'))
    
    return render_template("auth/user/update_profile.html", title="Update Profile", user=user)
