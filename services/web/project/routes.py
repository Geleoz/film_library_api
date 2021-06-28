from project import app
from flask import render_template
from project.models import Status, User


@app.route("/")
@app.route("/home")
def home_page():
    users = User.query.all()
    return render_template("home.html", users=users)
