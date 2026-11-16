"""Tests de services.py, sin pasar por HTTP."""

import pytest

from app.features.auth import services
from app.features.auth.models import User


def test_create_user_normalizes_name_and_email(app):
    user = services.create_user(
        name="  Luis ",
        email=" Luis@Example.com ",
        password="secreto123",
    )

    assert user.id is not None
    assert user.name == "Luis"
    assert user.email == "luis@example.com"
    assert user.password_hash != "secreto123"
    assert user.check_password("secreto123")
    assert not user.check_password("otra")


def test_create_user_defaults_to_alumno(app):
    user = services.create_user(
        name="Luis",
        email="luis@example.com",
        password="secreto123",
    )

    assert user.role == User.ROLE_ALUMNO


@pytest.mark.parametrize(
    "role",
    [User.ROLE_ALUMNO, User.ROLE_PROFESOR],
)
def test_create_user_accepts_valid_roles(app, role):
    user = services.create_user(
        name="Luis",
        email="luis@example.com",
        password="secreto123",
        role=role,
    )

    # También comprobamos que el rol se conserva al consultar la cuenta.
    saved_user = services.get_user_by_email("luis@example.com")

    assert saved_user is not None
    assert saved_user.id == user.id
    assert saved_user.role == role


@pytest.mark.parametrize(
    "role",
    ["admin", "administrador", "otro", "", None],
)
def test_create_user_rejects_invalid_roles(app, role):
    with pytest.raises(ValueError, match="El rol debe ser alumno o profesor"):
        services.create_user(
            name="Luis",
            email="luis@example.com",
            password="secreto123",
            role=role,
        )

    assert services.get_user_by_email("luis@example.com") is None


def test_create_user_rejects_duplicate_email(user):
    original_id = user.id
    original_name = user.name
    original_role = user.role
    original_hash = user.password_hash

    with pytest.raises(services.EmailAlreadyRegisteredError):
        services.create_user(
            name="Otra persona",
            email=f"  {user.email.upper()}  ",
            password="otra1234",
        )

    existing_user = services.get_user_by_email(user.email)

    assert existing_user.id == original_id
    assert existing_user.name == original_name
    assert existing_user.role == original_role
    assert existing_user.password_hash == original_hash


def test_can_create_another_user_after_duplicate_email(user):
    with pytest.raises(services.EmailAlreadyRegisteredError):
        services.create_user(
            name="Duplicado",
            email=user.email,
            password="secreto123",
        )

    new_user = services.create_user(
        name="Nueva persona",
        email="nueva@example.com",
        password="secreto123",
    )

    assert new_user.id is not None
    assert new_user.id != user.id


def test_get_user_by_email_normalizes_input(user):
    found = services.get_user_by_email(f"  {user.email.upper()}  ")

    assert found.id == user.id
    assert services.get_user_by_email("nadie@example.com") is None


@pytest.mark.parametrize("normalize_input", [False, True])
def test_authenticate_accepts_correct_credentials(user, normalize_input):
    email = (
        f"  {user.email.upper()}  "
        if normalize_input
        else user.email
    )

    authenticated_user = services.authenticate(email, "secreto123")

    assert authenticated_user is not None
    assert authenticated_user.id == user.id


def test_authenticate_rejects_wrong_password(user):
    assert services.authenticate(user.email, "otra") is None


def test_authenticate_rejects_unknown_email(app):
    assert services.authenticate(
        "nadie@example.com",
        "secreto123",
    ) is None
