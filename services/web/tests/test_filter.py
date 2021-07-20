from project.models import Film, Genre, Director
from datetime import datetime, date

def test_filter_by_genres():
    films = Film.query.filter(Film.genres.any(id=1))
    films = films.filter(Film.genres.any(id=2))
    genre1 = Genre.query.get(1)
    genre2 = Genre.query.get(2)
    for film in films:
        assert genre1 and genre2 in film.genres


def test_filter_by_release_date():
    films = Film.query.filter(
        Film.release_date.between("2010-01-01", "2020-01-01")
    )
    release_date_from = datetime.date(datetime.strptime("2010-01-01", "%Y-%m-%d"))
    release_date_to = datetime.date(datetime.strptime("2020-01-01", "%Y-%m-%d"))
    for film in films:
        print(film.release_date)
        assert film.release_date > release_date_from and film.release_date < release_date_to


def test_filter_by_director():
    films = Film.query.filter(Film.directors.any(id=1))
    director = Director.query.get(1)
    for film in films:
        assert director in film.directors
