"""
Lógica de negocio de la feature auth.

Las rutas llaman a estas funciones para consultar usuarios,
crear cuentas y comprobar credenciales.
"""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.extensions import db
from app.features.auth.models import User


class EmailAlreadyRegisteredError(ValueError):
    """El correo ya pertenece a una cuenta registrada."""


def normalize_email(email):
    return email.strip().lower()


def get_user_by_email(email):
    return db.session.scalar(
        db.select(User).where(User.email == normalize_email(email))
    )


def create_user(name, email, password, role=User.ROLE_ALUMNO):
    """Crea una cuenta con uno de los roles permitidos."""
    email = normalize_email(email)

    if role not in User.VALID_ROLES:
        raise ValueError("El rol debe ser alumno o profesor.")

    if get_user_by_email(email) is not None:
        raise EmailAlreadyRegisteredError(
            "Ya existe una cuenta con ese correo electrónico."
        )

    user = User(
        name=name.strip(),
        email=email,
        role=role,
    )
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()

        # Otra petición podría haber registrado el mismo correo
        # después de nuestra comprobación inicial.
        if get_user_by_email(email) is not None:
            raise EmailAlreadyRegisteredError(
                "Ya existe una cuenta con ese correo electrónico."
            ) from error

        # Conservamos otros errores de integridad para poder detectarlos.
        raise
    except SQLAlchemyError:
        db.session.rollback()
        raise

    return user


def authenticate(email, password):
    """Devuelve el usuario si las credenciales son correctas; si no, None."""
    user = get_user_by_email(email)

    if user is not None and user.check_password(password):
        return user

    return None