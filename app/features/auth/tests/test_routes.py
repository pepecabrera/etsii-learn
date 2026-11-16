"""Tests de registro, inicio y cierre de sesión."""

from urllib.parse import urlencode, urlsplit

import pytest
from flask import url_for

from app.features.auth import services
from app.features.auth.models import User


@pytest.fixture
def home_url(app):
    with app.test_request_context():
        return url_for("home.index")


def register_data(**overrides):
    """Datos válidos de registro, modificables para cada prueba."""
    data = {
        "name": "Luis",
        "email": "luis@example.com",
        "role": User.ROLE_ALUMNO,
        "password": "secreto123",
        "confirm": "secreto123",
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize(
    "role",
    [User.ROLE_ALUMNO, User.ROLE_PROFESOR],
)
def test_register_creates_user_and_logs_in(client, role):
    response = client.post(
        "/auth/register",
        data=register_data(role=role),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Tu cuenta se ha creado" in response.get_data(as_text=True)

    user = services.get_user_by_email("luis@example.com")
    assert user is not None
    assert user.role == role
    assert user.check_password("secreto123")
    assert user.password_hash != "secreto123"

    with client.session_transaction() as session:
        assert session["_user_id"] == str(user.id)


def test_register_rejects_duplicate_email(client, user):
    response = client.post(
        "/auth/register",
        data=register_data(email=user.email.upper()),
    )

    assert response.status_code == 200
    assert "Ya existe una cuenta" in response.get_data(as_text=True)

    with client.session_transaction() as session:
        assert "_user_id" not in session


@pytest.mark.parametrize("role", ["admin", "administrador", "otro"])
def test_register_rejects_invalid_role(client, role):
    response = client.post(
        "/auth/register",
        data=register_data(role=role),
    )

    assert response.status_code == 200
    assert services.get_user_by_email("luis@example.com") is None

    with client.session_transaction() as session:
        assert "_user_id" not in session


@pytest.mark.parametrize(
    "overrides",
    [
        {"name": ""},
        {"name": "   "},
        {"name": "a" * 81},
        {"email": "no-es-un-correo"},
        {"email": f"{'a' * 64}@{'b' * 50}.example.com"},
        {"password": "123", "confirm": "123"},
        {"password": "a" * 129, "confirm": "a" * 129},
        {"confirm": "otra-contraseña"},
    ],
)
def test_register_rejects_invalid_fields(client, overrides):
    data = register_data(**overrides)

    response = client.post("/auth/register", data=data)

    assert response.status_code == 200
    assert "is-invalid" in response.get_data(as_text=True)
    assert services.get_user_by_email(data["email"]) is None

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_register_shows_validation_errors_in_spanish(client):
    response = client.post(
        "/auth/register",
        data=register_data(
            name="",
            email="no-es-un-correo",
            confirm="otra-contraseña",
        ),
    )

    html = response.get_data(as_text=True)

    assert "Este campo es obligatorio." in html
    assert "Email inválido." in html
    assert "Las contraseñas no coinciden." in html


def test_register_normalizes_name_and_email(client):
    response = client.post(
        "/auth/register",
        data=register_data(
            name="  Luis  ",
            email="  LUIS@EXAMPLE.COM  ",
        ),
    )

    assert response.status_code == 302

    user = services.get_user_by_email("luis@example.com")
    assert user is not None
    assert user.name == "Luis"
    assert user.email == "luis@example.com"


def test_login_with_correct_password(client, user):
    response = client.post(
        "/auth/login",
        data={
            "email": f"  {user.email.upper()}  ",
            "password": "secreto123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert f"Hola de nuevo, {user.name}." in response.get_data(as_text=True)

    with client.session_transaction() as session:
        assert session["_user_id"] == str(user.id)


def test_login_with_wrong_password(client, user):
    response = client.post(
        "/auth/login",
        data={"email": user.email, "password": "mal"},
    )

    assert response.status_code == 200
    assert "Correo electrónico o contraseña incorrectos." in (
        response.get_data(as_text=True)
    )

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_login_with_unknown_email(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "desconocido@example.com",
            "password": "secreto123",
        },
    )

    assert response.status_code == 200
    assert "Correo electrónico o contraseña incorrectos." in (
        response.get_data(as_text=True)
    )

    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_login_redirects_to_next_page(client, user, home_url):
    destination = f"{home_url}?origen=login"
    query = urlencode({"next": destination})

    response = client.post(
        f"/auth/login?{query}",
        data={"email": user.email, "password": "secreto123"},
    )

    assert response.status_code == 302
    assert response.headers["Location"] == destination


@pytest.mark.parametrize(
    "destination",
    [
        "https://otro-sitio.com",
        "https:otro-sitio.com",
        "//otro-sitio.com",
        "/\\otro-sitio.com",
        "/\notro-sitio.com",
        "/ otro-sitio.com",
    ],
)
def test_login_rejects_unsafe_next_urls(
    client, user, home_url, destination
):
    query = urlencode({"next": destination})

    response = client.post(
        f"/auth/login?{query}",
        data={"email": user.email, "password": "secreto123"},
    )

    assert response.status_code == 302
    assert response.headers["Location"] == home_url


@pytest.mark.parametrize("path", ["/auth/login", "/auth/register"])
def test_authenticated_user_is_redirected(logged_client, home_url, path):
    response = logged_client.get(path)

    assert response.status_code == 302
    assert response.headers["Location"] == home_url


def test_logout(logged_client):
    response = logged_client.post(
        "/auth/logout",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Has cerrado sesión." in response.get_data(as_text=True)

    with logged_client.session_transaction() as session:
        assert "_user_id" not in session

    # Logout es una ruta protegida: sin sesión vuelve a pedir acceso.
    response = logged_client.post("/auth/logout")

    assert response.status_code == 302
    assert urlsplit(response.headers["Location"]).path == "/auth/login"


def test_logout_does_not_accept_get(logged_client):
    response = logged_client.get("/auth/logout")

    assert response.status_code == 405

    with logged_client.session_transaction() as session:
        assert "_user_id" in session


def test_register_requires_csrf_token(app, client):
    app.config["WTF_CSRF_ENABLED"] = True

    response = client.post(
        "/auth/register",
        data=register_data(),
    )

    assert response.status_code == 400
    assert services.get_user_by_email("luis@example.com") is None