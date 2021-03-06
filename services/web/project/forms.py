"""
Module contains form that displayed on the app pages
"""
from flask_wtf import FlaskForm
from wtforms import (
    widgets,
    StringField,
    TextAreaField,
    DecimalField,
    SelectMultipleField,
    SubmitField,
)
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, InputRequired, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from project.models import Director


def choose_directors():
    """
    Query all directors from db
    :return: list
    """
    return Director.query.all()


class MultiCheckboxField(SelectMultipleField):
    """
    Checkbox with multiple select options
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AddFilm(FlaskForm):
    """
    Form for adding films
    """
    title = StringField(
        label="Film title",
        validators=[
            InputRequired(message="Title not specified."),
            Length(min=2, max=64, message="Title must be 2 to 64 characters long."),
        ],
    )
    release_date = DateField(
        label="Release date",
        validators=[InputRequired(message="Release date not specified.")],
    )
    description = TextAreaField(
        label="Description",
        validators=[Length(max=4096, message="Description is too long.")],
    )
    rating = DecimalField(
        label="Rating",
        places=2,
        validators=[
            NumberRange(min=0.0, max=10.0, message="Rating must be between 0 and 10.")
        ],
    )
    poster = StringField(label="Poster url")
    director = QuerySelectField(
        label="Director", validators=[InputRequired()], query_factory=choose_directors
    )
    genre = MultiCheckboxField(
        label="Genres", validators=[InputRequired(message="Genres not specified.")]
    )
    submit = SubmitField(label="Confirm")


class FilterBy(FlaskForm):
    """
    Form for filtering films
    """
    release_date_from = DateField(label="Date From")
    release_date_to = DateField(label="Date To")
    director = QuerySelectField(
        label="Director", query_factory=choose_directors, allow_blank=True
    )
    genre = MultiCheckboxField(label="Genre")
    submit = SubmitField(label="Apply")
