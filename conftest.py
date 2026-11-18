"""
Fixtures compartidas de pytest.

Cada test utiliza una aplicación nueva y SQLite en memoria.
No se modifica la base de datos de desarrollo.

Durante cada test se mantiene un contexto de aplicación compartido.
Estas fixtures están pensadas para utilizar un cliente HTTP por test.
"""

import pytest

from app import create_app
from app.extensions import db
from app.features.auth import services as auth_services
from app.features.auth.models import User


@pytest.fixture
def app():
    """Aplicación de pruebas con una base de datos vacía."""
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "clave-exclusiva-de-tests",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "LOGIN_DISABLED": False,
            "SESSION_COOKIE_SECURE": False,
            "REMEMBER_COOKIE_SECURE": False,
        }
    )

    with app.app_context():
        db.create_all()

        try:
            yield app
        finally:
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


@pytest.fixture
def client(app):
    """Cliente HTTP que permite probar sin levantar un servidor."""
    return app.test_client()


@pytest.fixture
def user(app):
    """Alumno de prueba con contraseña secreto123."""
    return auth_services.create_user(
        name="Ana",
        email="ana@example.com",
        password="secreto123",
        role=User.ROLE_ALUMNO,
    )


@pytest.fixture
def logged_client(client, user):
    """Cliente autenticado como el alumno de prueba."""
    response = client.post(
        "/auth/login",
        data={
            "email": user.email,
            "password": "secreto123",
        },
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert session["_user_id"] == str(user.id)

    return client
