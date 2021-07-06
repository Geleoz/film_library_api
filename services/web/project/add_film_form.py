from flask_wtf import FlaskForm
from wtforms import widgets, StringField, TextAreaField, FloatField, SelectMultipleField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, EqualTo, Email, InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from project.models import Director, Genre


def choose_directors():
    return Director.query.all()


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddFilm(FlaskForm):
    title = StringField(label="Film title")
    release_date = DateField(label="Release date")
    description = TextAreaField(label="Description")
    rating = FloatField(label="Rating")
    poster = StringField(label="Poster url")
    director = QuerySelectField(label="Director", validators=[InputRequired()], query_factory=choose_directors)
    genre = MultiCheckboxField(label="Genres")
    submit = SubmitField(label="Add film")
