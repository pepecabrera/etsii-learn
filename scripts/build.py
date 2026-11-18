#!/usr/bin/env python3
"""Script de construcción de ETSII Learn.

Ejecuta, en este orden, las comprobaciones que debe pasar cualquier cambio
antes de integrarse en trunk:

1. Ficheros y configuración imprescindibles (sin imprimir valores secretos).
2. Linter y formato (ruff).
3. Pruebas (pytest).
4. Imagen Docker y pruebas dentro de la imagen.

Se detiene en el primer fallo y devuelve 0 solo si todo ha ido bien.

Uso:
    python scripts/build.py                  # todas las comprobaciones
    python scripts/build.py --skip-docker    # sin Docker (útil en local)
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGE = "etsii-learn:ci"
EN_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

FICHEROS_OBLIGATORIOS = [
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.prod.yml",
    "requirements.txt",
    "pyproject.toml",
    ".env.example",
    ".gitignore",
]

VARIABLES_OBLIGATORIAS = [
    "SECRET_KEY",
    "MARIADB_HOSTNAME",
    "MARIADB_PORT",
    "MARIADB_DATABASE",
    "MARIADB_USER",
    "MARIADB_PASSWORD",
    "MARIADB_ROOT_PASSWORD",
    "WEB_PORT",
]


def ejecutar(orden):
    """Ejecuta una orden en la raíz del proyecto y dice si ha ido bien."""
    return subprocess.run(orden, cwd=ROOT).returncode == 0


def comprobar_ficheros():
    faltan = [f for f in FICHEROS_OBLIGATORIOS if not (ROOT / f).is_file()]
    for fichero in faltan:
        print(f"Falta el fichero obligatorio: {fichero}")
    return not faltan


def comprobar_configuracion():
    """Comprueba .env.example y que .env no está versionado (sin mostrar valores)."""
    declaradas = set()
    for linea in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#") and "=" in linea:
            declaradas.add(linea.split("=", 1)[0].strip())
    faltan = [v for v in VARIABLES_OBLIGATORIAS if v not in declaradas]
    for variable in faltan:
        print(f"Falta la variable {variable} en .env.example")

    versionado = subprocess.run(
        ["git", "ls-files", "--error-unmatch", ".env"],
        cwd=ROOT,
        capture_output=True,
    )
    if versionado.returncode == 0:
        print(".env está versionado: debe quedar fuera del repositorio")
    return not faltan and versionado.returncode != 0


def linter():
    return ejecutar([sys.executable, "-m", "ruff", "check", "."])


def formato():
    return ejecutar([sys.executable, "-m", "ruff", "format", "--check", "."])


def pruebas():
    return ejecutar([sys.executable, "-m", "pytest", "-q"])


def construir_imagen():
    return ejecutar(["docker", "build", "-t", IMAGE, "."])


def pruebas_en_imagen():
    return ejecutar(["docker", "run", "--rm", IMAGE, "pytest", "-q"])


def main():
    parser = argparse.ArgumentParser(description="Construye y comprueba ETSII Learn.")
    parser.add_argument(
        "--skip-docker",
        action="store_true",
        help="no construir la imagen Docker ni probarla",
    )
    args = parser.parse_args()

    pasos = [
        ("Ficheros obligatorios", comprobar_ficheros),
        ("Configuración y secretos", comprobar_configuracion),
        ("Linter (ruff check)", linter),
        ("Formato (ruff format --check)", formato),
        ("Pruebas (pytest)", pruebas),
    ]
    if not args.skip_docker:
        pasos += [
            ("Imagen Docker", construir_imagen),
            ("Pruebas dentro de la imagen", pruebas_en_imagen),
        ]

    for numero, (nombre, paso) in enumerate(pasos, start=1):
        titulo = f"{numero}. {nombre}"
        print(f"::group::{titulo}" if EN_ACTIONS else f"\n== {titulo} ==", flush=True)
        correcto = paso()
        if EN_ACTIONS:
            print("::endgroup::", flush=True)
        if not correcto:
            if EN_ACTIONS:
                print(f"::error::Falla el paso {titulo}")
            print(f"\nFALLO en el paso {titulo}")
            return 1

    print("\nTodo correcto")
    return 0


if __name__ == "__main__":
    sys.exit(main())
