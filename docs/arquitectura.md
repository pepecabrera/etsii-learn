# Arquitectura

Una sola aplicación Flask con una base de datos MariaDB. Las páginas se generan en el servidor con Jinja y Bootstrap 5. No hay frontend separado ni API REST: un único servidor, una sesión de usuario y un único modelo de datos.

## Stack

| Componente | Uso |
| --- | --- |
| Python 3.13, Flask | Servidor y rutas, organizadas en blueprints con *application factory* |
| SQLAlchemy + PyMySQL | Acceso a MariaDB (InnoDB, utf8mb4) |
| Flask-Login | Sesiones y usuario actual |
| Flask-WTF | Formularios y protección CSRF |
| Werkzeug | Hash de contraseñas |
| Jinja + Bootstrap 5 (CDN) | Plantillas e interfaz |
| pytest, ruff | Pruebas y estilo |
| Docker Compose, GitHub Actions | Despliegue y CI |

Las versiones exactas se fijan en `requirements.txt` tras comprobar la instalación en Windows y macOS.

## Estructura

```text
etsii-learn/
  app/
    __init__.py        # create_app()
    config.py
    extensions.py      # db, login_manager, csrf
    cli.py             # comandos flask
    templates/base.html
    static/
    features/
      auth/            # Pepe
      asignaturas/     # José Ángel
      materiales/      # Vicente
      actividades/     # Rodrigo
      entregas/        # Pepe
      evaluacion/      # Lucas
      catalogo/        # Antonio
      aula/            # Antonio y Bruno
      agenda/          # Alfonso
      resultados/      # Pablo
  tests/
    conftest.py        # base de pruebas, cliente Flask y reloj controlado
    auth/              # una carpeta por feature, con el mismo nombre
    asignaturas/
    materiales/
    actividades/
    entregas/
    evaluacion/
    catalogo/
    aula/
    agenda/
    resultados/
    acceptance/        # ciclo completo entre módulos de ambos equipos
  scripts/build.py
  docs/
  Dockerfile
  compose.yaml
  requirements.txt
  requirements-dev.txt
  .env.example
```

Cada módulo de `features/` contiene solo lo que necesita:

```text
routes.py     # peticiones HTTP
forms.py      # formularios (Flask-WTF)
services.py   # reglas de negocio y permisos
models.py     # tablas SQLAlchemy (solo en el módulo propietario)
templates/    # plantillas del módulo
```

## Pruebas

Cada feature tiene su carpeta en `tests/` con el mismo nombre que su módulo, de modo que cada persona trabaja y revisa solo sus pruebas. Dentro de cada carpeta:

- `test_services.py`: reglas de negocio y permisos.
- `test_routes.py`: rutas, formularios y respuestas con MariaDB de pruebas.

`tests/acceptance/` contiene el recorrido completo (publicar, entregar, evaluar, consultar), que implica a varios módulos. Se usa siempre MariaDB real, nunca SQLite, y una base aislada distinta de la normal.

## Capas

| Capa | Hace | No hace |
| --- | --- | --- |
| Ruta | Lee el formulario, llama al servicio, renderiza o redirige | Reglas de negocio ni consultas |
| Servicio | Comprueba permisos y reglas, confirma o deshace la transacción | Fiarse del rol o usuario enviado por el navegador |
| Modelo | Define tablas y relaciones | Abrir transacciones |
| Plantilla | Muestra datos | Decidir permisos |

Un módulo no escribe en las tablas de otro: usa las funciones de su servicio. Si un contrato cambia, se abre un WI y se avisa a los consumidores.

## Configuración

`create_app()` crea la aplicación, carga la configuración y registra blueprints, CSRF y Flask-Login. Importar un módulo no debe crear tablas ni insertar datos.

| Variable | Uso |
| --- | --- |
| `SECRET_KEY` | Firma de sesiones y CSRF; obligatoria, sin valor por defecto |
| `DB_HOST`, `DB_PORT`, `DB_NAME` | Conexión a MariaDB (en Compose, `DB_HOST=db`) |
| `DB_USER`, `DB_PASSWORD` | Usuario de la aplicación, sin privilegios globales |
| `TEST_DB_NAME` | Base de pruebas, distinta de `DB_NAME` y terminada en `_test` |

`.env` no se versiona ni entra en la imagen Docker. `.env.example` contiene solo valores de ejemplo.

## Comandos

| Comando | Qué hace |
| --- | --- |
| `flask db-upgrade` | Crea o actualiza el esquema sin borrar datos |
| `flask seed-demo` | Carga datos ficticios (solo en desarrollo; no duplica al repetirse) |

Las cuentas de profesor dependen de la decisión pendiente de alta de profesores (registro en la demo o comando de gestión).

## Rutas y errores

- Las lecturas usan GET; crear, modificar y borrar usan POST con CSRF.
- Tras una escritura correcta se redirige, para evitar reenvíos al recargar.
- Dos equipos no registran la misma ruta.

| Situación | Respuesta |
| --- | --- |
| Sin sesión en página privada | Redirige al acceso |
| Sin permiso | 403 |
| No existe | 404 |
| Formulario inválido | Vuelve al formulario con los errores |
| Plazo cerrado, duplicado o estado incompatible | 409 con explicación |
| Fallo inesperado | 500 genérico, sin detalles internos |

## Seguridad

- Contraseñas con hash de Werkzeug, nunca en claro.
- CSRF en todos los formularios que modifican datos.
- Jinja escapa el texto; no usar `|safe` con contenido de usuarios.
- Rol, pertenencia a la asignatura y propietario se comprueban en el servidor en cada operación.
- Consultas siempre parametrizadas (SQLAlchemy lo hace por defecto).
- Debug solo en local.

## Fechas

Se guardan en UTC y se muestran en `Europe/Madrid`. El servidor decide si un plazo está abierto. En pruebas el reloj se sustituye por configuración, nunca por un parámetro de la petición.

## Construcción, CI y Docker

- `python scripts/build.py` es el script de construcción propio del proyecto; los pasos están en el README. CI lo ejecuta con cada push.
- Docker Compose levanta `web` (Flask, puerto 5000) y `db` (MariaDB con volumen persistente). `web` espera a que la base esté disponible, y las migraciones se ejecutan como paso explícito.
- No se incluyen `.env`, `.git` ni entornos virtuales en la imagen. Las imágenes se fijan por versión, no con `latest`.
- Servir el proyecto en Internet (WSGI y HTTPS) queda fuera del alcance.