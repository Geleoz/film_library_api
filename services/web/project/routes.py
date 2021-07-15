from project import app, db
from flask import render_template, redirect, url_for, flash
from project.models import Status, User, Film
from project.auth import RegisterForm, LoginForm
from flask_login import login_user, logout_user


@app.route("/")
@app.route("/home")
def home_page():
    films = Film.query.all()
    return render_template("home.html", films=films)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password1.data,
                        status_id=1)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Error: {err}.", category="danger")
    return render_template("auth/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("home_page"))
        flash("Wrong username or password", category="danger")
    return render_template("auth/login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for("home_page"))
