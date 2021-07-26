from project import db
from project.models import Film

def test_search_by_title():
    query = "%the%"
    films = Film.query.filter(Film.title.ilike(query))
    for film in films:
        assert "the" in film.title.lower()


def test_search_by_release_date():
    query = "%1994%"
    films = Film.query.filter(db.cast(Film.release_date, db.String(10)).ilike(query))
    for film in films:
        assert "1994" in str(film.release_date)


def test_search_by_raiting():
    query = "%8.6%"
    films = Film.query.filter(db.cast(Film.rating, db.String(10)).ilike(query))
    for film in films:
        assert float(film.rating) == 8.6
