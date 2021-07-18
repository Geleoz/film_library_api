from project import db, login_manager, admin
from sqlalchemy.orm import relationship
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    added_films = relationship("Film", back_populates="user")
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    def __repr__(self):
        return f"{self.username} {self.roles}"

    def is_admin(self):
        return Role.query.get(2) in self.roles

    def get_id(self):
        return self.id


film_director = db.Table(
    "film_director",
    db.Column("film_id", db.Integer, db.ForeignKey("film.id", ondelete="SET NULL")),
    db.Column(
        "director_id", db.Integer, db.ForeignKey("director.id", ondelete="SET NULL")
    ),
)


class Director(db.Model):
    __tablename__ = "director"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birth_date = db.Column(db.Date)
    films = relationship("Film", secondary=film_director, back_populates="directors")

    def __repr__(self):
        return self.first_name + " " + self.last_name


film_genre = db.Table(
    "film_genre",
    db.Column("film_id", db.Integer, db.ForeignKey("film.id", ondelete="SET NULL")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id", ondelete="SET NULL")),
)


class Genre(db.Model):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    films = relationship(
        "Film", secondary=film_genre, back_populates="genres", cascade="all, delete"
    )

    def __repr__(self):
        return self.name


class Film(db.Model):
    __tablename__ = "film"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.Numeric, nullable=False)
    poster = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = relationship("User", back_populates="added_films")
    directors = relationship(
        "Director", secondary=film_director, back_populates="films"
    )
    genres = relationship(
        "Genre", secondary=film_genre, back_populates="films", passive_deletes=True
    )

    def __repr__(self):
        return self.title
