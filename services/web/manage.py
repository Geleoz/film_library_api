from flask.cli import FlaskGroup
from project import app, db
from project.models import User, Director, Genre, Film
from numpy import genfromtxt
import pandas as pd


cli = FlaskGroup(app)


def load_data(file_path):
    data = genfromtxt(file_path, delimiter=',', converters={0: lambda s: str(s)}, dtype=None, encoding=None)
    return data.tolist()


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    # try:
    # directors = load_data("project/data/directors.csv")
    # genres = load_data("project/data/genres.csv")
    # films = load_data("project/data/films.csv")
    # film_director = load_data("project/data/film_director.csv")
    # film_genre = load_data("project/data/film_genre.csv")
    directors = pd.read_csv("project/data/directors.csv", quotechar='"', skipinitialspace=True, header=None)
    genres = pd.read_csv("project/data/genres.csv", quotechar='"', skipinitialspace=True, header=None)
    films = pd.read_csv("project/data/films.csv", quotechar='"', skipinitialspace=True, header=None)
    film_director = pd.read_csv("project/data/film_director.csv", quotechar='"', skipinitialspace=True, header=None)
    film_genre = pd.read_csv("project/data/film_genre.csv", quotechar='"', skipinitialspace=True, header=None)

    for i in directors.itertuples():
        director = Director(**{
            "first_name": i[1],
            "last_name": i[2],
            "birth_date": i[3]
        })
        db.session.add(director)

    for i in genres.itertuples():
        genre = Genre(**{
            "name": i[1]
        })
        db.session.add(genre)

    current_film_id = 1
    for i in films.itertuples():
        film = Film(**{
            "title": i[1],
            "release_date": i[2],
            "description": i[3],
            "rating": i[4],
            "poster": i[5]
        })
        for j in film_director.itertuples():
            if j[1] == current_film_id:
                film.directors.append(Director.query.filter_by(id=j[2]).first())
        for j in film_genre.itertuples():
            if j[1] == current_film_id:
                film.genres.append(Genre.query.filter_by(id=j[2]).first())
        db.session.add(film)
        current_film_id += 1

    db.session.commit()

    # for i in film_director.itertuples():
    #     print(i[0], i[1])
    #     statement = film_director.insert().values((i[1],), (i[2],))
    #     db.session.execute(statement)
        #db.session.connection().execute(film_director.insert(), params={"film_id": i[1], "director_id": i[2]},)

    # for i in film_genre.itertuples():
    #     db.session.connection().execute(film_genre.insert().values(film_id=i[1], genre_id=i[2]))

    # except:
    #     db.session.rollback()
    # db.session.add(User(username="user_name", email="user_email@gmail.com", password="pass"))
    # director = Director(first_name="Christopher", last_name="Nolan", birth_date="1970-07-30")
    # db.session.add(director)
    # action = Genre(name="Action")
    # adventure = Genre(name="Adventure")
    # sci_fi = Genre(name="Sci-Fi")
    # db.session.add(action)
    # db.session.add(adventure)
    # db.session.add(sci_fi)
    # inception = Film(title="Inception", release_date="2010-07-22", description="""
    # Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction,
    # stealing valuable secrets from deep within the subconscious during the dream state,
    # when the mind is at its most vulnerable. Cobb's rare ability has made him a coveted
    # player in this treacherous new world of corporate espionage, but it has also made him
    # an international fugitive and cost him everything he has ever loved. Now Cobb is being
    # offered a chance at redemption. One last job could give him his life back but only if
    # he can accomplish the impossible, inception. Instead of the perfect heist, Cobb and his
    # team of specialists have to pull off the reverse: their task is not to steal an idea, but
    # to plant one. If they succeed, it could be the perfect crime. But no amount of careful planning
    # or expertise can prepare the team for the dangerous enemy that seems to predict their every move.
    # An enemy that only Cobb could have seen coming.
    # """, rating=8.8, poster="https://images-na.ssl-images-amazon.com/images/I/912AErFSBHL._SL1500_.jpg", user_id=1)
    # inception.directors.append(director)
    # inception.genres.append(action)
    # inception.genres.append(adventure)
    # inception.genres.append(sci_fi)
    # db.session.add(inception)
    # db.session.commit()


if __name__ == "__main__":
    cli()
