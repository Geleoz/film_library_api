from project.models import Film


def test_sort_by_release_date():
    films = Film.query.order_by(Film.release_date)
    prev_release_date = None
    for film in films:
        if prev_release_date:
            assert prev_release_date <= film.release_date
        prev_release_date = film.release_date


def test_sort_by_rating():
    films = Film.query.order_by(Film.rating)
    prev_rating = None
    for film in films:
        if prev_rating:
            assert prev_rating <= film.rating
        prev_rating = film.rating
