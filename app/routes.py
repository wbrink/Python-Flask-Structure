from flask import render_template, flash, redirect, url_for, request
from app import app, db 
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post

# home
@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="zzzzz")

# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in")
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit(): 
        #flash('Login requested for user {}, remember_me={}'.format( form.username.data, form.remember_me.data)) 
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        # login_required decorator will intercept and redirect to login view 
        # and will add query string argument to the url 
        next_page = request.args.get("next") # getting the 'next' query string
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", form=form ) 

# logout
@app.route('/logout') 
def logout(): 
    logout_user() 
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data) 
        user.set_password(form.password.data) 
        db.session.add(user) 
        db.session.commit() 
        flash('Congratulations, you are now a registered user!') 
        return redirect(url_for('login')) 
    return render_template("register.html", form=form)