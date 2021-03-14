from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(max=16)],
        render_kw={"placeholder": "Enter a nickname for your household"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Choose a strong password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords do not match."),
        ],
        render_kw={"placeholder": "Re-enter your password"},
    )

    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    username = StringField(
        "Household nickname",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter nick"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
