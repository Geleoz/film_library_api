from project import app
from flask import render_template
from project.models import Film


@app.route("/")
@app.route("/home")
def home_page():
    films = Film.query.all()
    return render_template("home.html", films=films)
