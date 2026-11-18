"""Cuentas ficticias con contraseña pública para desarrollo y pruebas."""

from app.features.auth import services
from app.features.auth.models import User

DEMO_PASSWORD = "Prueba1234"

DEMO_USERS = [
    {
        "name": "Ana Torres",
        "email": "ana.profesor@example.com",
        "role": User.ROLE_PROFESOR,
    },
    {
        "name": "Luis Romero",
        "email": "luis.profesor@example.com",
        "role": User.ROLE_PROFESOR,
    },
    {
        "name": "Marta López",
        "email": "marta.alumno@example.com",
        "role": User.ROLE_ALUMNO,
    },
    {
        "name": "Pablo García",
        "email": "pablo.alumno@example.com",
        "role": User.ROLE_ALUMNO,
    },
    {
        "name": "Elena Ruiz",
        "email": "elena.alumno@example.com",
        "role": User.ROLE_ALUMNO,
    },
]


def seed():
    """Crea las cuentas que faltan sin modificar las existentes."""
    for data in DEMO_USERS:
        existing_user = services.get_user_by_email(data["email"])

        if existing_user is not None:
            if existing_user.role != data["role"]:
                raise ValueError(f"La cuenta {data['email']} ya existe con otro rol.")
            continue

        services.create_user(
            name=data["name"],
            email=data["email"],
            password=DEMO_PASSWORD,
            role=data["role"],
        )
