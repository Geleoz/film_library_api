from project import app, db
from flask import render_template, redirect, url_for, flash
from project.models import Status, User
from project.auth import RegisterForm


@app.route("/")
@app.route("/home")
def home_page():
    users = User.query.all()
    return render_template("home.html", users=users)


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
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Error: {err}.", category="danger")
    return render_template("register.html", form=form)
