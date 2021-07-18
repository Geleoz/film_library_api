"""
Flask app routes
"""
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from flasgger.utils import swag_from
from project import app, db, login_manager
from project.models import Film, Genre, Director, User, Role
from project.forms import AddFilm, FilterBy
from project.auth import RegisterForm, LoginForm


def get_filtered_films():
    """
    Returns films filtered by parameter stored in sessions
    :return: list of Film objects
    """
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
    """
    Returns films sorted by sort_parameter
    Sorts all films if films parameter is None
    :param sort_parameter: string
    :param films: list of Film objects
    :return: list of Film objects
    """
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


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
@swag_from("static/home.yml")
def home_page():
    """
    Home page
    :return: html template
    """
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
@swag_from("static/search_get.yml", methods=["GET"])
@swag_from("static/search_post.yml", methods=["POST"])
def search_page():
    """
    Search page
    :return:
        - redirect to the route
        - html template
    """
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
@swag_from("static/filter_get.yml", methods=["GET"])
@swag_from("static/filter_post.yml", methods=["POST"])
def filter_page():
    """
    Filter page
    :return: html template
    """
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


@app.route("/sort", methods=["POST"])
@swag_from("static/sort.yml")
def sort_page():
    """
    Sort page
    :return: redirect to another route
    """
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
    if "filter" in request.args:
        return redirect(url_for("filter_page", filter=True, sort=sort))
    # if sort home page
    return redirect(url_for("home_page", sort=sort))


@app.route("/<film_id>/<film_title>")
@swag_from("static/film_page.yml")
def film_page(film_id, film_title):
    """
    Film page
    :param film_id: int
    :param film_title: string
    :return: html template
    """
    film = Film.query.filter_by(id=film_id).first()
    return render_template("film_page.html", film=film)


@app.route("/add_film", methods=["GET", "POST"])
@login_required
@swag_from("static/add_film_get.yml", methods=["GET"])
@swag_from("static/add_film_post.yml", methods=["POST"])
def add_film_page():
    """
    Add film page
    :return:
        - redirect to another route
        - html template
    """
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
            flash(f"Error: {err}.", category="danger")
    return render_template("add_film.html", form=form)


@app.route("/delete_film", methods=["POST"])
@swag_from("static/delete_film.yml")
def delete_film_page():
    """
    Delete film page
    :return: redirect to another route
    """
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
@swag_from("static/register_get.yml", methods=["GET"])
@swag_from("static/register_post.yml", methods=["POST"])
def register_page():
    """
    Register page
    :return:
        - redirect to another route
        - html template
    """
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
            flash(f"Error: {err[0]}", category="danger")
    return render_template("auth/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
@swag_from("static/login_get.yml", methods=["GET"])
@swag_from("static/login_post.yml", methods=["POST"])
def login_page():
    """
    Login page
    :return:
        - redirect to another route
        - html template
    """
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
    """
    Called when unauthorized user tries to go to the route with @login_required decorator
    :return: redirect to /login route
    """
    flash(
        "Please sign in or create new account to perform this action.",
        category="danger"
    )
    return redirect("/login")


@app.route("/logout")
@login_required
@swag_from("static/logout.yml")
def logout_page():
    """
    Logout page
    :return: redirect to another route
    """
    app.logger.info(f"User logout: {current_user.username}")
    logout_user()
    return redirect(url_for("home_page"))
