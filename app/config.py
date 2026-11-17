"""
Configuración de ETSII Learn.

Las variables de entorno pueden definirse en .env durante el desarrollo.
Los valores por defecto están pensados para desarrollo local.
"""

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = "ETSII Learn"

    # Firma las sesiones y los tokens CSRF.
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "clave-de-desarrollo-cambiame",
    )

    # Utilizamos las traducciones de WTForms mediante Meta.locales,
    # sin integrar Flask-Babel.
    WTF_I18N_ENABLED = False
    WTF_CSRF_ENABLED = True

    # Cookies de sesión y de la opción «Recordarme».
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"

    # Conexión a MariaDB configurable mediante variables de entorno.
    MARIADB_HOSTNAME = os.getenv("MARIADB_HOSTNAME", "localhost")
    MARIADB_PORT = os.getenv("MARIADB_PORT", "3306")
    MARIADB_DATABASE = os.getenv("MARIADB_DATABASE", "etsii_learn_db")
    MARIADB_USER = os.getenv("MARIADB_USER", "etsii_user")
    MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "etsii_password")

    # DATABASE_URL tiene prioridad sobre las variables MARIADB_*.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        f"mysql+pymysql://"
        f"{quote_plus(MARIADB_USER)}:{quote_plus(MARIADB_PASSWORD)}"
        f"@{MARIADB_HOSTNAME}:{MARIADB_PORT}/{MARIADB_DATABASE}"
        f"?charset=utf8mb4"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
