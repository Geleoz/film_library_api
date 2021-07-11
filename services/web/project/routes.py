from project import app, db
from flask import render_template, request, flash, redirect, url_for, session
from project.models import Film, Genre, Director
from project.forms import AddFilm, FilterBy


def get_sorted_filtered_films():
    if "query" in session:
        films = Film.query.filter(Film.title.ilike(session["query"]) |
                                  db.cast(Film.release_date, db.String(10)).ilike(session["query"]) |
                                  db.cast(Film.rating, db.String(10)).ilike(session["query"]))
    else:
        if "release_date_from" not in session or not session["release_date_from"]:
            session["release_date_from"] = Film.query.order_by(Film.release_date).first().release_date
        if "release_date_to" not in session or not session["release_date_to"]:
            session["release_date_to"] = Film.query.order_by(Film.release_date.desc()).first().release_date
        films = Film.query.filter(Film.release_date.between(session["release_date_from"], session["release_date_to"]))
        if "director" in session and session["director"] != "__None":
            films = films.filter(Film.directors.any(id=session["director"]))
        if "genres" in session:
            for genre_id in session["genres"]:
                films = films.filter(Film.genres.any(id=genre_id))

    if "sort" in session:
        if session["sort"] == "sort_by_release_date_asc":
            films = films.order_by(Film.release_date)
        elif session["sort"] == "sort_by_release_date_desc":
            films = films.order_by(Film.release_date.desc())
        elif session["sort"] == "sort_by_rating_asc":
            films = films.order_by(Film.rating)
        elif session["sort"] == "sort_by_rating_desc":
            films = films.order_by(Film.rating.desc())
    return films


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home_page():
    session.clear()
    form = FilterBy()
    form.genre.choices = [(str(x.id), x.name) for x in Genre.query.all()]

    page = request.args.get('page', 1, type=int)

    if form.is_submitted() and "query" not in request.form:
        session["release_date_from"] = request.form["release_date_from"]
        session["release_date_to"] = request.form["release_date_to"]
        session["director"] = request.form["director"]
        session["genres"] = []
        for genre_id in form.genre.data:
            session["genres"].append(genre_id)
        return redirect(url_for("filter_page"))

    if request.method == "POST":
        session["query"] = f"%{request.form['query']}%"
        return redirect(url_for("search_page"))
    films = Film.query.paginate(page=page, per_page=10)
    return render_template("home.html", films=films, form=form)


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


@app.route("/search", methods=["GET", "POST"])
def search_page():
    form = FilterBy()
    form.genre.choices = [(str(x.id), x.name) for x in Genre.query.all()]
    page = request.args.get('page', 1, type=int)

    if form.is_submitted() and "query" not in request.form:
        session["release_date_from"] = request.form["release_date_from"]
        session["release_date_to"] = request.form["release_date_to"]
        session["director"] = request.form["director"]
        session["genres"] = []
        for genre_id in form.genre.data:
            session["genres"].append(genre_id)
        return redirect(url_for("filter_page"))

    if request.method == "POST" and "query" in request.form:
        query = request.form["query"]
        query = f"%{query}%"
        session["query"] = query
    else:
        query = session["query"]

    films = Film.query.filter(Film.title.ilike(query) |
                              db.cast(Film.release_date, db.String(10)).ilike(query) |
                              db.cast(Film.rating, db.String(10)).ilike(query)).paginate(page=page,
                                                                                         per_page=10)

    return render_template("search.html", form=form, films=films, query=query)


@app.route("/filter", methods=["GET", "POST"])
def filter_page():
    form = FilterBy()
    form.genre.choices = [(str(x.id), x.name) for x in Genre.query.all()]
    page = request.args.get('page', 1, type=int)

    if form.is_submitted() and "query" not in request.form:
        session["release_date_from"] = request.form["release_date_from"]
        session["release_date_to"] = request.form["release_date_to"]
        session["director"] = request.form["director"]
        session["genres"] = []
        for genre_id in form.genre.data:
            session["genres"].append(genre_id)

    if request.method == "POST" and "query" in request.form:
        session["query"] = f"%{request.form['query']}%"
        return redirect(url_for("search_page"))

    films = get_sorted_filtered_films().paginate(page=page, per_page=10)
    return render_template("filter.html", films=films, form=form)


@app.route("/sort", methods=["GET", "POST"])
def sort_page():
    form = FilterBy()
    form.genre.choices = [(str(x.id), x.name) for x in Genre.query.all()]
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        if "sort_by_release_date_asc" in request.form:
            session["sort"] = "sort_by_release_date_asc"
        elif "sort_by_release_date_desc" in request.form:
            session["sort"] = "sort_by_release_date_desc"
        if "sort_by_rating_asc" in request.form:
            session["sort"] = "sort_by_rating_asc"
        elif "sort_by_rating_desc" in request.form:
            session["sort"] = "sort_by_rating_desc"

        films = get_sorted_filtered_films().paginate(page=page, per_page=10)
        if "query" in session:
            return render_template("search.html", films=films, form=form)
        return render_template("filter.html", films=films, form=form)
