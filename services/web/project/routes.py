from project import app
from flask import render_template
from project.models import Film, Genre
from project.add_film_form import AddFilm


@app.route("/")
@app.route("/home")
def home_page():
    films = Film.query.all()
    return render_template("home.html", films=films)


@app.route("/<film_id>/<film_title>", methods=["GET"])
def film_page(film_id, film_title):
    film = Film.query.filter_by(id=film_id).first()
    return render_template("film_page.html", film=film)


@app.route("/add_film", methods=["GET", "POST"])
def add_film_page():
    form = AddFilm()
    form.genre.choices = [(x, x) for x in Genre.query.all()]
    return render_template("add_film.html", form=form)
