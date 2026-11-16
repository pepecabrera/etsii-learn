"""
Comandos de consola propios:

    flask init-db   → crea las tablas que no existen
    flask seed-db   → carga los datos de ejemplo de autenticación
    flask reset-db  → borra las tablas, las recrea y carga ejemplos
"""

import click

from app.extensions import db
from app.features.auth import seeders as auth_seeders


def seed_all():
    """Carga los datos de ejemplo de las features habilitadas."""
    auth_seeders.seed()


def register_commands(app):
    @app.cli.command("init-db")
    def init_db():
        """Crea las tablas de los modelos importados por la aplicación."""
        db.create_all()
        click.echo("Tablas creadas; las existentes se han conservado.")

    @app.cli.command("seed-db")
    def seed_db():
        """Carga los datos de ejemplo de autenticación."""
        seed_all()
        click.echo("Carga de datos de ejemplo completada.")

    @app.cli.command("reset-db")
    @click.confirmation_option(
        prompt=(
            "Esto borra TODAS las tablas de los modelos cargados "
            "y sus datos. ¿Continuar?"
        )
    )
    def reset_db():
        """Elimina las tablas, las recrea y carga los datos de ejemplo."""
        db.session.remove()
        db.drop_all()
        db.create_all()
        seed_all()
        click.echo("Base de datos reiniciada.")
