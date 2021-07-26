"""
Module for creating database and filling it with initial values
"""
from flask.cli import FlaskGroup
import pandas as pd
from project import app, db
from project.models import User, Director, Genre, Film, Role


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    """
    Creates db
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """
    Fills in db with initial values
    """
    user_role = Role(name="user")
    admin_role = Role(name="admin")
    db.session.add(user_role)
    db.session.add(admin_role)
    db.session.add(
        User(
            username="admin",
            email="admin@gmail.com",
            password="adminpassword",
            roles=[user_role, admin_role],
        )
    )
    db.session.add(
        User(
            username="username",
            email="email@gmail.com",
            password="password",
            roles=[user_role],
        )
    )
    directors = pd.read_csv(
        "project/data/directors.csv", quotechar='"', skipinitialspace=True, header=None
    )
    genres = pd.read_csv(
        "project/data/genres.csv", quotechar='"', skipinitialspace=True, header=None
    )
    films = pd.read_csv(
        "project/data/films.csv", quotechar='"', skipinitialspace=True, header=None
    )
    film_director = pd.read_csv(
        "project/data/film_director.csv",
        quotechar='"',
        skipinitialspace=True,
        header=None,
    )
    film_genre = pd.read_csv(
        "project/data/film_genre.csv", quotechar='"', skipinitialspace=True, header=None
    )

    for i in directors.itertuples():
        director = Director(
            **{"first_name": i[1], "last_name": i[2], "birth_date": i[3]}
        )
        db.session.add(director)

    for i in genres.itertuples():
        genre = Genre(**{"name": i[1]})
        db.session.add(genre)

    current_film_id = 1
    for i in films.itertuples():
        film = Film(
            **{
                "title": i[1],
                "release_date": i[2],
                "description": i[3],
                "rating": i[4],
                "poster": i[5],
                "user_id": 1
            }
        )
        for j in film_director.itertuples():
            if j[1] == current_film_id:
                film.directors.append(Director.query.filter_by(id=j[2]).first())
        for j in film_genre.itertuples():
            if j[1] == current_film_id:
                film.genres.append(Genre.query.filter_by(id=j[2]).first())
        db.session.add(film)
        current_film_id += 1
    db.session.commit()
    db.session.commit()


if __name__ == "__main__":
    cli()
