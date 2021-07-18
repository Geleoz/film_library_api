"""
Module with authentication forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, EqualTo, Email, InputRequired
from project.models import User


class RegisterForm(FlaskForm):
    """
    Form with registration fields
    """
    def validate_username(self, new_username):
        """
        Checks entered username for uniqueness
        :param new_username: string
        :raise: ValidationError if user with such username already exists
        """
        user = User.query.filter_by(username=new_username.data).first()
        if user:
            raise ValidationError("Username already exists.")

    def validate_email(self, new_email):
        """
        Checks entered email for uniqueness
        :param new_email: string
        :raise: ValidationError if user with such email already exists
        """
        user = User.query.filter_by(email=new_email.data).first()
        if user:
            raise ValidationError("Email already exists.")

    username = StringField(
        label="Username",
        validators=[
            Length(
                min=2,
                max=32,
                message="Username must be between 2 and 32 characters long.",
            )
        ],
    )
    email = StringField(label="Email", validators=[Email()])
    password1 = PasswordField(
        label="Password",
        validators=[
            Length(
                min=6,
                max=64,
                message="Password must be between 6 and 64 characters long.",
            )
        ],
    )
    password2 = PasswordField(
        label="Confirm password",
        validators=[EqualTo("password1", message="Password mismatch.")],
    )
    submit = SubmitField(label="Create account")


class LoginForm(FlaskForm):
    """
    Form with login fields
    """
    username = StringField(label="Username", validators=[InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    submit = SubmitField(label="Sign-In")
