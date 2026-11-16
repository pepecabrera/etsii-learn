"""Tests de los comandos de poblado y reinicio."""

from app.extensions import db
from app.features.auth import services as auth_services
from app.features.auth.models import User
from app.features.auth.seeders import DEMO_PASSWORD, DEMO_USERS


def assert_demo_users():
    """Comprueba las cinco cuentas y sus roles."""
    users = db.session.scalars(db.select(User)).all()

    assert len(users) == 5
    assert sum(user.is_profesor for user in users) == 2
    assert sum(user.is_alumno for user in users) == 3

    for data in DEMO_USERS:
        user = auth_services.get_user_by_email(data["email"])

        assert user is not None
        assert user.name == data["name"]
        assert user.role == data["role"]
        assert user.check_password(DEMO_PASSWORD)


def test_seed_db_creates_demo_data_only_once(app):
    runner = app.test_cli_runner()

    result = runner.invoke(args=["seed-db"])
    assert result.exit_code == 0, result.output

    original_ids = {user.email: user.id for user in db.session.scalars(db.select(User)).all()}

    result = runner.invoke(args=["seed-db"])
    assert result.exit_code == 0, result.output

    assert_demo_users()

    current_ids = {user.email: user.id for user in db.session.scalars(db.select(User)).all()}
    assert current_ids == original_ids


def test_reset_db_starts_from_scratch(app, user):
    # Conservamos el correo antes del reinicio, que desconecta los objetos.
    previous_email = user.email
    runner = app.test_cli_runner()

    result = runner.invoke(args=["reset-db", "--yes"])

    assert result.exit_code == 0, result.output
    assert auth_services.get_user_by_email(previous_email) is None
    assert_demo_users()
