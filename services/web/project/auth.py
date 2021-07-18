from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, EqualTo, Email, InputRequired
from project.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, new_username):
        user = User.query.filter_by(username=new_username.data).first()
        if user:
            raise ValidationError("Username already exists")

    def validate_email(self, new_email):
        user = User.query.filter_by(email=new_email.data).first()
        if user:
            raise ValidationError("Email already exists")

    username = StringField(label="Username", validators=[Length(min=2, max=32)])
    email = StringField(label="Email", validators=[Email()])
    password1 = PasswordField(label="Password", validators=[Length(min=6, max=64)])
    password2 = PasswordField(
        label="Confirm password", validators=[EqualTo("password1")]
    )
    submit = SubmitField(label="Create account")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[InputRequired()])
    password = PasswordField(label="Password", validators=[InputRequired()])
    submit = SubmitField(label="Sign-In")
