"""Rutas de registro, inicio y cierre de sesión."""

from flask import flash, redirect, render_template, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app.features.auth import auth_bp, services
from app.features.auth.forms import LoginForm, RegisterForm


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = services.create_user(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                role=form.role.data,
            )
        except services.EmailAlreadyRegisteredError as error:
            form.email.errors.append(str(error))
        else:
            login_user(user)
            flash(
                f"Te damos la bienvenida, {user.name}. "
                "Tu cuenta se ha creado.",
                "success",
            )
            return redirect(url_for("home.index"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = services.authenticate(
            email=form.email.data,
            password=form.password.data,
        )

        if user is None:
            flash(
                "Correo electrónico o contraseña incorrectos.",
                "danger",
            )
        else:
            login_user(user, remember=form.remember.data)
            flash(f"Hola de nuevo, {user.name}.", "success")
            return redirect(safe_next_url())

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("home.index"))


def safe_next_url():
    """Acepta únicamente rutas locales para volver después del acceso."""
    next_url = request.args.get("next", "")
    fallback = url_for("home.index")

    if not next_url.startswith("/") or next_url.startswith("//"):
        return fallback

    # Evita barras inversas y caracteres que puedan alterar
    # la interpretación de la URL en el navegador.
    if "\\" in next_url:
        return fallback

    if any(ord(character) <= 32 or ord(character) == 127 for character in next_url):
        return fallback

    return next_url