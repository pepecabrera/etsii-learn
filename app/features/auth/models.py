from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """Usuario registrado con rol de alumno o profesor."""

    __tablename__ = "users"

    ROLE_ALUMNO = "alumno"
    ROLE_PROFESOR = "profesor"
    VALID_ROLES = (ROLE_ALUMNO, ROLE_PROFESOR)

    __table_args__ = (
        db.CheckConstraint(
            "role IN ('alumno', 'profesor')",
            name="ck_users_role",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.String(20),
        nullable=False,
        default=ROLE_ALUMNO,
        server_default=ROLE_ALUMNO,
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        # Se guarda en UTC sin zona horaria, compatible con DATETIME.
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )

    @validates("email")
    def normalize_email(self, key, email):
        """Guarda el correo sin espacios externos y en minúsculas."""
        return email.strip().lower()

    @validates("role")
    def validate_role(self, key, role):
        """Solo admite los dos roles definidos por la aplicación."""
        if role not in self.VALID_ROLES:
            raise ValueError("El rol debe ser alumno o profesor.")
        return role

    @property
    def is_alumno(self):
        return self.role == self.ROLE_ALUMNO

    @property
    def is_profesor(self):
        return self.role == self.ROLE_PROFESOR

    def set_password(self, password):
        """Almacena el hash de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Comprueba la contraseña contra el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User id={self.id} role={self.role}>"


@login_manager.user_loader
def load_user(user_id):
    """Recupera el usuario asociado a la sesión."""
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None

    if user_id <= 0:
        return None

    return db.session.get(User, user_id)