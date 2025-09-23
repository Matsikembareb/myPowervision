from myPowervision import app
from flask import render_template, session, url_for, redirect, flash, request
from myPowervision.forms import LoginForm
from myPowervision import bcrypt
from myPowervision.models import User
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
@app.route("/admin")
def adminIndex():
    return render_template("auth/admin/index.html", title="Admin Login")

# ---------------------------------user area--------------------------------------

# user login
@app.route("/user", methods=['GET', 'POST'])
def userIndex():
    if request.method == 'POST':
        # process the form data
        email = request.form.get('email')
        password = request.form.get('password')

        user = User().query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            approval = User().query.filter_by(id=user.id).first()
            if approval.status == 0:
                flash("Your account is not approved by admin yet.", "warning")
                return redirect(url_for('userIndex'))
            else:
                session['user_id'] = user.id
                session['username'] = user.username
                flash("Login Success", "success")
                return redirect(url_for('userIndex'))
        else:
            flash("Invalid credentials. Please check all the fields", "danger")
            return redirect(url_for('userIndex'))
        
    return render_template("auth/user/index.html", title="User Login")

# user registration
@app.route("/user/signup", methods=['GET', 'POST'])
def userSignup():
    if request.method == 'POST':
        print("Form submitted!")  # Debug print
        # process the form data
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        username = request.form.get('username')
        edu = request.form.get('edu')
        password = request.form.get('password')

        if fname == '' or lname == '' or email == '' or username == '' or edu == '':
            flash("Please fill all the fields", "danger")
            return redirect(url_for('userSignup'))
        else:
            is_email = User().query.filter_by(email=email).first()
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
    else:
        return render_template("auth/user/signup.html", title="User Signup")

#user dashboard
@app.route("/user/dashboard")
def userDashboard():
    if session.get('username'):
        return f'{session["username"]}'
    #if 'user_id' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('userIndex'))
    return render_template("auth/user/dashboard.html", title="User Dashboard")