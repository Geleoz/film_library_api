from project import app
from flask import render_template
from project.models import Film


@app.route("/")
@app.route("/home")
def home_page():
    films = Film.query.all()
    return render_template("home.html", films=films)


@app.route("/<film_id>/<film_title>", methods=["GET"])
def film_page(film_id, film_title):
    film = Film.query.filter_by(film_id=film_id).first()
    return render_template("film_page.html", film=film)
