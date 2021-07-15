from flask.cli import FlaskGroup
from project import app, db
from project.models import User, Director, Genre, Film


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(username="user_name", email="user_email@gmail.com", password="pass"))
    director = Director(first_name="first_name", last_name="last_name", birth_date="2021-07-04")
    genre1 = Genre(name="genre1")
    genre2 = Genre(name="genre2")
    db.session.add(Film(title="film", release_date="2021-07-04", description="desc", rating=8, poster="poster", user_id="1"))
    director.films.append(Film.query.filter_by(film_id=1).first())
    genre1.films.append(Film.query.filter_by(film_id=1).first())
    genre2.films.append(Film.query.filter_by(film_id=1).first())
    db.session.add(director)
    db.session.add(genre1)
    db.session.add(genre2)
    db.session.commit()


if __name__ == "__main__":
    cli()
