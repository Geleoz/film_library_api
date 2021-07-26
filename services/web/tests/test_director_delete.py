from project import db
from project.models import Film, Director


def test_director_delete_with_film_attached():
    director = Director(first_name="first_name", last_name="last_name")
    db.session.add(director)
    film = Film(title="test", release_date="01-01-2021",
                description="description", rating=8, poster="poster")
    film.directors.append(director)
    db.session.add(film)
    db.session.commit()
    director_id = director.id
    film_id = film.id
    Director.query.filter_by(id=director_id).delete()
    assert Film.query.get(film_id)
    Film.query.filter_by(id=film_id).delete()
    db.session.commit()