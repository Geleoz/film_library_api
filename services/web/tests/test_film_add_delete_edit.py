from project import db
from project.models import Film, Genre, Director
from decorator import decorator
from flask.testing import FlaskClient


def test_add_film_page_unauthorized(client):
    response = client.get("/add_film")
    assert response.status_code == 302


def login_user(sess, user_id):
    sess['_user_id'] = user_id


@decorator
def force_login(func, cb=None, *args, **kwargs):
    for arg in args:
        if isinstance(arg, FlaskClient):
            with arg:
                with arg.session_transaction() as sess:
                    cb(sess)
            return func(*args, **kwargs)
    return func(*args, **kwargs)


@force_login(cb=lambda s: login_user(s, 2))
def test_add_film_page_authorized(client):
    res = client.get("/add_film")
    assert res.status_code == 200


def test_delete_unauthorized(test_client):
    test_client.post("/delete_film?film_id=1")
    assert Film.query.get(1)


@force_login(cb=lambda s: login_user(s, 2))
def test_delete_authorized(client):
    client.post("/delete_film?film_id=1")
    assert Film.query.get(1)


@force_login(cb=lambda s: login_user(s, 2))
def test_delete_authorized_with_adding(client):
    director = Director.query.get(1)
    genre1 = Genre.query.get(1)
    genre2 = Genre.query.get(2)
    film = Film(title="test", release_date="01-01-2021",
                description="description", rating=8, poster="poster", user_id=2)
    film.directors.append(director)
    film.genres.append(genre1)
    film.genres.append(genre2)
    db.session.add(film)
    db.session.commit()
    film_id = film.id
    client.post(f"/delete_film?film_id={film_id}")
    assert not Film.query.get(film_id)


def test_add_unauthorized(test_client):
    response = test_client.post("/add_film",
                                data={
                                    "title": "title",
                                    "release_date": "01-01-2021",
                                    "description": "description",
                                    "rating": "8",
                                    "poster": "poster",
                                    "director": "1"
                                })
    assert response.status_code == 302


@force_login(cb=lambda s: login_user(s, 2))
def test_add_authorized(client):
    response = client.post("/add_film",
                           data={
                               "title": "title",
                               "release_date": "01-01-2021",
                               "description": "description",
                               "rating": "8",
                               "poster": "poster",
                               "director": "1"
                           })
    assert response.status_code == 200


def test_edit_unauthorized(test_client):
    response = test_client.get("/edit_film")
    assert response.location.endswith("/login")
    response = test_client.post("/edit_film?film_id=1", data={
        "title": "title",
        "release_date": "01-01-2021",
        "description": "desc",
        "rating": "8",
        "poster": "poster",
        "director": "1"
    })
    assert response.location.endswith("/login")


@force_login(cb=lambda s: login_user(s, 2))
def test_edit_authorized(client):
    response = client.get("/edit_film")
    assert response.location.endswith("/home")
    response = client.post("/edit_film?film_id=1", data={
        "title": "title",
        "release_date": "01-01-2021",
        "description": "desc",
        "rating": "8",
        "poster": "poster",
        "director": "1"
    })
    assert response.location.endswith("/home")
