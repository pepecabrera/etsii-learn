# ETSII Learn · Arquitectura y stack tecnológico

Versión 0.1 · 13 de noviembre de 2026 · Propuesta de implementación.

**Estado:** este documento define la estructura objetivo. Los módulos, scripts, comandos y contenedores descritos todavía no están incluidos en el paquete documental.

## 1. Enfoque

Una sola aplicación Flask organizada en módulos y una base de datos MariaDB. Se renderizan páginas HTML con Jinja. JavaScript mejora filtros o formularios cuando aporta valor; no se construye una aplicación frontend independiente ni una API REST completa por defecto.

Esta estructura permite repartir funcionalidades completas sin mantener dos servidores, dos sesiones de usuario o dos copias del modelo académico.

## 2. Stack propuesto

| Componente | Decisión inicial | Motivo |
| --- | --- | --- |
| Python | Serie 3.12 | Base común propuesta para desarrollo, CI y contenedor. |
| Flask | Serie 3.1 | Servidor y rutas, con módulos Blueprint. |
| Jinja | Incluido con Flask | Plantillas compartidas y páginas renderizadas en servidor. |
| MariaDB | Serie 11.4, InnoDB y utf8mb4 | Persistencia relacional compartida. |
| PyMySQL | Versión exacta por fijar | Acceso SQL desde Python; soporte de MariaDB. |
| Flask-WTF | Serie 1.2 | Validación de formularios y protección CSRF. |
| python-dotenv | Versión exacta por fijar | Carga local de configuración de desarrollo. |
| Werkzeug | Dependencia compatible con Flask | Funciones de hash y comprobación de contraseñas. |
| HTML, CSS y JavaScript | Sin framework de frontend | Tecnologías de la asignatura y menor carga inicial. |
| pytest | Versión exacta por fijar | Pruebas de reglas, rutas e integración. |
| Docker Compose | Compose v2 | Aplicación y MariaDB con configuración reproducible. |
| GitHub Actions | Workflow con push | Pruebas y construcción independientes de las PRs. |

Las series son una propuesta de arranque, no una afirmación de que sean las versiones más recientes. En el hito 1 se verificará la instalación en Windows y macOS y se fijarán versiones exactas de paquetes e imágenes. Si la asignatura impone otras versiones, registrar el ajuste y repetir la prueba de instalación.

No se mezclará SQL directo y un ORM en distintas áreas. La propuesta inicial es SQL parametrizado con PyMySQL. Cambiar a un ORM requiere una decisión conjunta antes de crear las tablas y servicios.

## 3. Organización prevista

La estructura siguiente es orientativa; solo README y los seis documentos de docs existen en este paquete.

~~~text
etsii-learn/
  README.md
  requirements.txt
  requirements-dev.txt
  .env.example
  .gitignore
  .dockerignore
  Dockerfile
  compose.yaml
  .github/
    ISSUE_TEMPLATE/
      work-item.yml
    workflows/
      ci.yml
  app/
    __init__.py
    config.py
    db.py
    cli.py
    auth/
    asignaturas/
    materiales/
    actividades/
    entregas/
    evaluacion/
    panel/
    templates/
      base.html
      components/
    static/
      css/
        tokens.css
        components.css
      js/
  sql/
    migrations/
      001_schema.sql
  scripts/
    build.py
  tests/
    conftest.py
    unit/
    integration/
    acceptance/
  docs/
    producto.md
    organizacion.md
    arquitectura.md
    datos-e-integracion.md
    diseno.md
    roadmap-y-calidad.md
~~~

Cada módulo funcional puede contener routes.py, forms.py, service.py y repository.py. No crear capas vacías sin necesidad, pero conservar una separación clara entre HTTP, reglas de negocio y SQL.

## 4. Responsabilidades técnicas

| Capa | Responsabilidad | Evitar |
| --- | --- | --- |
| Ruta Flask | Leer el formulario, recuperar el usuario autenticado, invocar el servicio y renderizar o redirigir. | SQL y reglas duplicadas en cada ruta. |
| Servicio | Validar permisos y reglas y delimitar la transacción de una operación. | Confiar en el usuario o rol enviado por el navegador. |
| Repositorio | Ejecutar SQL parametrizado sobre la conexión recibida. | Abrir transacciones o confirmar cambios por su cuenta. |
| Plantilla | Presentar datos escapados y componentes comunes. | Consultar la base o decidir permisos reales. |
| JavaScript | Mejorar interacción y mostrar validaciones complementarias. | Convertirse en la única validación de permisos o fechas. |

Los servicios de escritura son los puntos de entrada transaccionales. Si necesitan lógica de otro módulo, utilizan funciones de lectura o validación sin commit sobre la misma conexión. No anidar servicios que abran transacciones independientes.

## 5. Arranque y configuración

La función create_app(test_config=None) crea la aplicación, carga configuración, registra Blueprints, configura CSRF y prepara cierre de conexiones. Importar un módulo no debe crear tablas ni insertar datos.

La autenticación guarda únicamente el identificador necesario en la sesión. En cada petición privada se recupera el usuario actual y su rol desde el servidor. No guardar contraseñas, entregas o notas en la cookie de sesión.

| Variable propuesta | Uso |
| --- | --- |
| SECRET_KEY | Firma de sesiones y CSRF; obligatoria y distinta por entorno. |
| DB_HOST / DB_PORT | Dirección de MariaDB; en Compose, DB_HOST será db. |
| DB_NAME | Base de desarrollo o demostración. |
| DB_USER / DB_PASSWORD | Credenciales del usuario de aplicación, sin privilegios de administración global. |
| TEST_DB_NAME | Base aislada de pruebas, distinta de DB_NAME y con sufijo _test. |
| APP_TIMEZONE | Europe/Madrid para entrada y presentación. |
| LOG_LEVEL | Nivel de registro, sin incluir datos privados o secretos. |

El archivo .env.example contiene nombres y valores de ejemplo no sensibles. .env queda fuera de Git y de la imagen Docker. La aplicación falla con un mensaje de configuración útil si falta una variable obligatoria; no utiliza una clave secreta constante por defecto.

Conservar fechas UTC en MariaDB. Al interpretar un formulario local, convertir desde Europe/Madrid y rechazar horas inexistentes o ambiguas por cambios de horario. Los servicios trabajan con instantes UTC y un reloj sustituible en pruebas.

## 6. Base de datos y evolución del esquema

- Una única definición inicial del esquema, acordada entre A2, A4, B3 y A5.
- Scripts SQL numerados y un registro de migraciones aplicadas.
- No editar retroactivamente una migración que ya utilicen ambos equipos; añadir otra.
- Configuración común de InnoDB, utf8mb4, colación y modo SQL.
- Consultas parametrizadas para todos los valores. Los nombres de columnas de ordenación se seleccionan de una lista permitida.
- Claves foráneas, índices y restricciones descritos en [Datos e integración](datos-e-integracion.md).
- Los repositorios no conocen contraseñas ni crean conexiones alternativas para eludir transacciones.

Comandos de gestión previstos:

| Comando Flask | Contrato |
| --- | --- |
| db-upgrade | Aplica migraciones pendientes en orden y registra el resultado; no borra datos existentes. |
| seed-demo | Crea datos ficticios coherentes solo en un entorno de desarrollo o demostración; no duplica los datos si se repite. |
| create-professor | Crea una cuenta docente de forma controlada y solicita la contraseña sin guardarla en Git. |

MariaDB puede confirmar implícitamente operaciones DDL. El aplicador no prometerá rollback total de una migración de esquema: deberá registrar fallos y detenerse sin continuar a ciegas.

## 7. Convenciones de rutas y errores

Las rutas usan nombres coherentes en español y url_for para enlazarse. Las lecturas utilizan GET; las mutaciones usan POST y CSRF. No habrá operaciones de borrar, aceptar o evaluar mediante GET.

Tras una escritura válida se realiza una redirección 303 para evitar repetir el envío al recargar. Las validaciones fallidas conservan los campos y muestran mensajes asociados.

| Situación | Respuesta prevista |
| --- | --- |
| Sin sesión en una página privada | Redirección al acceso; comprobar que la URL de retorno sea local. |
| Usuario autenticado sin permiso | 403 con página comprensible. |
| Recurso inexistente | 404. |
| Formulario inválido | 422 con errores visibles. |
| CSRF ausente o inválido | 400. |
| Plazo cerrado, duplicado o estado incompatible | 409 con explicación. |
| Fallo inesperado | 500 genérico y registro interno sin secretos. |

Las mismas reglas deben aplicarse si se añade una respuesta JSON. No se exige JSON para completar el MVP.

## 8. Seguridad necesaria para el ciclo

- Hash de contraseñas mediante las funciones de Werkzeug; nunca texto plano.
- CSRF en formularios y peticiones JavaScript que cambian datos.
- Escape de texto en Jinja; no aplicar safe a contenido de alumnos o profesores.
- Renderizar contenido recibido con textContent cuando corresponda en JavaScript.
- Comprobar rol, pertenencia a la asignatura y propietario de cada recurso.
- Evitar enlaces javascript: u otros esquemas no permitidos.
- Cookies HttpOnly y SameSite; Secure cuando se utilice HTTPS.
- Modo debug solo en desarrollo local.
- Usuario de base de datos de aplicación con permisos limitados.

Si se incorporan archivos: guardarlos fuera de static, generar nombres internos, limitar tamaño, validar el contenido permitido y servirlos mediante una ruta con permisos. Añadirlos requiere actualizar pruebas y despliegue.

## 9. Construcción y CI previstas

El punto de entrada será python scripts/build.py. Será un script propio, portable entre Windows y macOS y reutilizado por CI.

Secuencia prevista:

1. Validar archivos y configuración necesarios sin imprimir secretos.
2. Comprobar que TEST_DB_NAME identifica una base de pruebas y difiere de la base normal.
3. Preparar o migrar únicamente esa base aislada.
4. Ejecutar pytest con las pruebas unitarias, de integración y del ciclo completo.
5. Construir la imagen de la aplicación con Docker.
6. Devolver cero únicamente si todas las etapas son correctas.

Las dependencias se instalan previamente a partir de ficheros versionados. El script no debe borrar una base que el usuario haya indicado arbitrariamente. La limpieza se limita al entorno de pruebas verificado.

CI se ejecuta con cada push de las ramas activas y puede activarse en PRs entre equipos. Prepara Python, MariaDB y variables de prueba, ejecuta el mismo script y conserva el resultado de pruebas. Una construcción correcta de una rama no sustituye comprobar el resultado de su integración.

## 10. Docker y ejecución local

Dos servicios previstos:

- web: imagen propia de Flask, puerto local 5000, configuración por entorno.
- db: MariaDB, comprobación de disponibilidad y volumen persistente.

El servicio web debe esperar a que la base esté disponible, no solo a que el contenedor haya arrancado. Las migraciones son un paso explícito y repetible. No depender exclusivamente de scripts de inicialización que solo se ejecutan cuando el volumen está vacío.

El despliegue académico local puede utilizar el servidor de desarrollo en localhost. Una publicación accesible desde Internet requeriría definir servidor WSGI y HTTPS; no forma parte del alcance actual.

No incluir .env, .git, entornos virtuales ni datos locales en el contexto final de la imagen. No utilizar etiquetas latest como sustituto de fijar las versiones comprobadas.

## 11. Registro inicial de decisiones

| ID | Decisión | Estado |
| --- | --- | --- |
| D01 | Una aplicación Flask y una base MariaDB | Propuesta inicial |
| D02 | Jinja y JavaScript sin framework | Restricción del proyecto |
| D03 | SQL parametrizado con PyMySQL, sin ORM | Propuesta inicial |
| D04 | Sesión común, roles y permisos en servidor | Necesario para el producto |
| D05 | Entregas de texto; PDF como ampliación | Propuesta de alcance |
| D06 | Evaluación tras el cierre y actividad bloqueada con entregas | Propuesta que deben revisar ambos equipos |
| D07 | Modelo Git | Pendiente de instrucciones docentes |

## 12. Referencias técnicas

Consultadas el 13 de noviembre de 2026. Sirven como apoyo de implementación; no demuestran que el proyecto ya esté construido.

- [Instalación de Flask](https://flask.palletsprojects.com/en/stable/installation/).
- [Application factories en Flask](https://flask.palletsprojects.com/en/stable/patterns/appfactories/).
- [Instalación y compatibilidad de PyMySQL](https://pymysql.readthedocs.io/en/latest/user/installation.html).
- [CSRF en Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/csrf/).
- [Política de mantenimiento de MariaDB](https://mariadb.org/about/#maintenance-policy).
- [Workflows de GitHub Actions](https://docs.github.com/en/actions/tutorials/create-an-example-workflow).
- [Docker Compose](https://docs.docker.com/compose/).
