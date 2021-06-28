from project import app, db
from flask import render_template, request, flash, redirect, url_for
from project.models import Film, Genre, Director
from project.add_film_form import AddFilm


@app.route("/")
@app.route("/home")
def home_page():
    page = request.args.get("page", 1, type=int)
    films = Film.query.paginate(page=page, per_page=10)
    return render_template("home.html", films=films)


@app.route("/<film_id>/<film_title>", methods=["GET"])
def film_page(film_id, film_title):
    film = Film.query.filter_by(id=film_id).first()
    return render_template("film_page.html", film=film)


@app.route("/add_film", methods=["GET", "POST"])
def add_film_page():
    form = AddFilm()
    form.genre.choices = [(str(x.id), x.name) for x in Genre.query.all()]
    if form.validate_on_submit():
        film = Film(title=request.form["title"],
                    release_date=request.form["release_date"],
                    description=request.form["description"],
                    rating=request.form["rating"],
                    poster=request.form["poster"])
        film.directors.append(Director.query.filter_by(id=request.form["director"]).first())
        for genre_id in form.genre.data:
            film.genres.append(Genre.query.filter_by(id=genre_id).first())
        db.session.add(film)
        db.session.commit()
        flash("Film has been added successfully.", category="success")
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err in form.errors.values():
            for i in form.genre.data:
                flash(i, category="danger")
            flash(f"Error: {err}.", category="danger")
    return render_template("add_film.html", form=form)
