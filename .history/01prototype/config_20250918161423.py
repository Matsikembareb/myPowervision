import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6e0e0a43d505c3d5e496b4cc'#TO BE CHANGED TO you-will-never-guess
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'ums.sqlite')#TO BE CONVERTED TO APP.DB
    SESSION_PERMANENT = False#CHANGE IN PRODUCTION
    SESSION_TYPE = 'filesystem'#CHANGE IN PRODUCTION

# user login
@app.route("/user", methods=['GET', 'POST'])
def userIndex():
    if request.method == 'POST':
        # process the form data
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # Remove ()
        if user and bcrypt.check_password_hash(user.password, password):
            if user.status == 0:  # 0 means not approved, 1 means approved
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
            is_email = User.query.filter_by(email=email).first()  # Remove ()
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