from myPowervision import app
from flask import render_template, url_for, redirect, flash
from myPowervision.forms import LoginForm

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






@app.route("/admin/")
def adminIndex():
    return render_template("auth/admin/index.html", title="Admin Login")

@app.route("/user/")
def userIndex():
    return render_template("auth/user/index.html", title="User Login")

@app.route("/UMS")
def index():
    return render_template("auth/index.html")
