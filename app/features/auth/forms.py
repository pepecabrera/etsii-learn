from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.features.auth.models import User


def strip_spaces(value):
    """Elimina espacios al principio y al final."""
    return value.strip() if value is not None else value


def normalize_email(value):
    """Aplica el mismo criterio de correo en registro y acceso."""
    return value.strip().lower() if value is not None else value


class RegisterForm(FlaskForm):
    class Meta:
        locales = ["es"]

    name = StringField(
        "Nombre",
        filters=[strip_spaces],
        validators=[
            DataRequired(),
            Length(max=80),
        ],
    )

    email = EmailField(
        "Correo electrónico",
        filters=[normalize_email],
        validators=[
            DataRequired(),
            Length(max=120),
            Email(),
        ],
    )

    role = SelectField(
        "Tipo de cuenta",
        choices=[
            (User.ROLE_ALUMNO, "Alumno"),
            (User.ROLE_PROFESOR, "Profesor"),
        ],
        default=User.ROLE_ALUMNO,
        validators=[DataRequired()],
        validate_choice=True,
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(min=6, max=128),
        ],
    )

    confirm = PasswordField(
        "Repite la contraseña",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Las contraseñas no coinciden.",
            ),
        ],
    )

    submit = SubmitField("Crear cuenta")


class LoginForm(FlaskForm):
    class Meta:
        locales = ["es"]

    email = EmailField(
        "Correo electrónico",
        filters=[normalize_email],
        validators=[
            DataRequired(),
            Length(max=120),
            Email(),
        ],
    )

    password = PasswordField(
        "Contraseña",
        validators=[DataRequired()],
    )

    remember = BooleanField("Recordarme")

    submit = SubmitField("Entrar")