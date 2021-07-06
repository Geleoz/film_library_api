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
    director = Director(first_name="Christopher", last_name="Nolan", birth_date="1970-07-30")
    db.session.add(director)
    action = Genre(name="Action")
    adventure = Genre(name="Adventure")
    sci_fi = Genre(name="Sci-Fi")
    db.session.add(action)
    db.session.add(adventure)
    db.session.add(sci_fi)
    inception = Film(title="Inception", release_date="2010-07-22", description="""
    Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction, 
    stealing valuable secrets from deep within the subconscious during the dream state, 
    when the mind is at its most vulnerable. Cobb's rare ability has made him a coveted 
    player in this treacherous new world of corporate espionage, but it has also made him 
    an international fugitive and cost him everything he has ever loved. Now Cobb is being
    offered a chance at redemption. One last job could give him his life back but only if 
    he can accomplish the impossible, inception. Instead of the perfect heist, Cobb and his
    team of specialists have to pull off the reverse: their task is not to steal an idea, but
    to plant one. If they succeed, it could be the perfect crime. But no amount of careful planning
    or expertise can prepare the team for the dangerous enemy that seems to predict their every move. 
    An enemy that only Cobb could have seen coming.
    """, rating=8.8, poster="https://images-na.ssl-images-amazon.com/images/I/912AErFSBHL._SL1500_.jpg", user_id=1)
    inception.directors.append(director)
    inception.genres.append(action)
    inception.genres.append(adventure)
    inception.genres.append(sci_fi)
    #director.films.append(Film.query.filter_by(film_id=1).first())
    #action.films.append(Film.query.filter_by(film_id=1).first())
    #adventure.films.append(Film.query.filter_by(film_id=1).first())
    #sci_fi.films.append(Film.query.filter_by(film_id=1).first())
    db.session.add(inception)
    db.session.commit()


if __name__ == "__main__":
    cli()
