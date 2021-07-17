from project import app, db, admin, login_manager
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from project.models import Film, Genre, Director, User, Role
from project.forms import AddFilm, FilterBy
from project.auth import RegisterForm, LoginForm


def get_filtered_films():
    if "release_date_from" not in session or not session["release_date_from"]:
        session["release_date_from"] = (
            Film.query.order_by(Film.release_date).first().release_date
        )
    if "release_date_to" not in session or not session["release_date_to"]:
        session["release_date_to"] = (
            Film.query.order_by(Film.release_date.desc()).first().release_date
        )
    films = Film.query.filter(
        Film.release_date.between(
            session["release_date_from"], session["release_date_to"]
        )
    )
    if "director" in session and session["director"] != "__None":
        films = films.filter(Film.directors.any(id=session["director"]))
    if "genres" in session:
        for genre_id in session["genres"]:
            films = films.filter(Film.genres.any(id=genre_id))
    return films


def get_sorted_films(sort_parameter, films=None):
    if not films:
        films = Film.query
    if sort_parameter == "sort_by_release_date_asc":
        films = films.order_by(Film.release_date)
    elif sort_parameter == "sort_by_release_date_desc":
        films = films.order_by(Film.release_date.desc())
    elif sort_parameter == "sort_by_rating_asc":
        films = films.order_by(Film.rating)
    elif sort_parameter == "sort_by_rating_desc":
        films = films.order_by(Film.rating.desc())
    return films


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home_page():
    form = FilterBy()
    form.genre.choices = [(str(x.id), x.name) for x in Genre.query.all()]

    page = request.args.get("page", 1, type=int)

    # if sort
    if "sort" in request.args:
        sort = request.args.get("sort")
        films = get_sorted_films(sort).paginate(page=page, per_page=10)
        return render_template("home.html", films=films, form=form, sort=sort)

    # just home page with all films
    films = Film.query.paginate(page=page, per_page=10)
    return render_template("home.html", films=films, form=form)


@app.route("/search", methods=["GET", "POST"])
def search_page():
    # receives requests from base.html or search.html

    page = request.args.get("page", 1, type=int)

    # if search
    if "query" in request.form:
        query = f"%{request.form['query']}%"
        return redirect(url_for("search_page", key=query))

    query = request.args.get("key")
    films = Film.query.filter(
        Film.title.ilike(query)
        | db.cast(Film.release_date, db.String(10)).ilike(query)
        | db.cast(Film.rating, db.String(10)).ilike(query)
    )

    # if sort search results
    if "sort" in request.args:
        sort = request.args.get("sort")
        films = get_sorted_films(sort, films).paginate(page=page, per_page=10)
        return render_template("search.html", films=films, key=query, sort=sort)

    # if just switch page
    films = films.paginate(page=page, per_page=10)
    return render_template("search.html", films=films, key=query)


@app.route("/filter", methods=["GET", "POST"])
def filter_page():
    # receives requests from home.html or filter.html

    form = FilterBy()
    form.genre.choices = [(str(x.id), x.name) for x in Genre.query.all()]
    page = request.args.get("page", 1, type=int)

    # if filter
    if form.is_submitted():
        session["release_date_from"] = request.form["release_date_from"]
        session["release_date_to"] = request.form["release_date_to"]
        session["director"] = request.form["director"]
        session["genres"] = []
        for genre_id in form.genre.data:
            session["genres"].append(genre_id)

    films = get_filtered_films()

    # if sort filtered films
    if "sort" in request.args:
        sort = request.args.get("sort")
        films = get_sorted_films(sort, films).paginate(page=page, per_page=10)
        return render_template(
            "filter.html", films=films, form=form, filter=True, sort=sort
        )

    # if just switch page
    films = films.paginate(page=page, per_page=10)
    return render_template("filter.html", films=films, form=form, filter=True)


@app.route("/sort", methods=["GET", "POST"])
def sort_page():
    # receives requests from home.html, search.html or filter.html

    # by default sort = "sort_by_release_date_asc"
    sort = "sort_by_release_date_asc"
    if "sort_by_release_date_desc" in request.form:
        sort = "sort_by_release_date_desc"
    elif "sort_by_rating_asc" in request.form:
        sort = "sort_by_rating_asc"
    elif "sort_by_rating_desc" in request.form:
        sort = "sort_by_rating_desc"

    # if sort search page
    if "key" in request.args:
        return redirect(url_for("search_page", key=request.args.get("key"), sort=sort))
    # if sort filter page
    elif "filter" in request.args:
        return redirect(url_for("filter_page", filter=True, sort=sort))
    # if sort home page
    return redirect(url_for("home_page", sort=sort))


@app.route("/<film_id>/<film_title>", methods=["GET"])
def film_page(film_id, film_title):
    film = Film.query.filter_by(id=film_id).first()
    return render_template("film_page.html", film=film)


@app.route("/add_film", methods=["GET", "POST"])
@login_required
def add_film_page():
    form = AddFilm()
    form.genre.choices = [(str(x.id), x.name) for x in Genre.query.all()]
    if form.validate_on_submit():
        film = Film(
            title=request.form["title"],
            release_date=request.form["release_date"],
            description=request.form["description"],
            rating=request.form["rating"],
            poster=request.form["poster"],
            user_id=current_user.get_id(),
        )
        film.directors.append(
            Director.query.filter_by(id=request.form["director"]).first()
        )
        for genre_id in form.genre.data:
            film.genres.append(Genre.query.filter_by(id=genre_id).first())
        db.session.add(film)
        db.session.commit()
        flash("Film has been added successfully.", category="success")
        app.logger.info(
            f"New film added by user {current_user.username}: {film}(id: {film.id})"
        )
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err in form.errors.values():
            for i in form.genre.data:
                flash(i, category="danger")
            flash(f"Error: {err}.", category="danger")
    return render_template("add_film.html", form=form)


@app.route("/delete_film", methods=["POST"])
def delete_film_page():
    app.logger.info(
        f"Film {Film.query.get(request.args.get('film_id'))}"
        f"(id: {request.args.get('film_id')}) "
        f"has been deleted by {current_user.username}"
    )
    Film.query.filter_by(id=request.args.get("film_id")).delete()
    db.session.commit()
    flash("Film has been deleted successfully.", category="success")
    return redirect(url_for("home_page"))


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password1.data,
            roles=[Role.query.get(1)],
        )
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"New user registered: {new_user.username}")
        login_user(new_user)
        app.logger.info(f"User {new_user.username} logged in successfully")
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
            app.logger.info(f"User {user.username} logged in successfully")
            return redirect(url_for("home_page"))
        flash("Wrong username or password", category="danger")
    return render_template("auth/login.html", form=form)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash(
        "Unauthorized users cannot add films. Please sign in or create new account.",
        category="danger",
    )
    return redirect("/login")


@app.route("/logout")
def logout_page():
    app.logger.info(f"User logout: {current_user.username}")
    logout_user()
    return redirect(url_for("home_page"))
