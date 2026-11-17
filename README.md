# ETSII Learn

Plataforma abierta y sencilla para gestionar clases y tareas, con dos roles: **profesor** y **alumno**. Alternativa simple a productos como Blackboard.

**Flujo principal:** el profesor crea una asignatura → el alumno solicita unirse → el profesor acepta y publica una actividad → el alumno entrega antes del cierre → el profesor corrige y devuelve la nota → el alumno la consulta.

> **Estado:** planificación. Todavía no hay código, base de datos, contenedores ni pruebas. Los comandos de este README son los que deberán funcionar tras el primer hito.

## Equipos

| Equipo | Integrantes | Enfoque |
| --- | --- | --- |
| A · Profesores | José Ángel, Lucas, Rodrigo, Vicente, Adrián | Asignaturas, materiales, actividades y evaluación |
| B · Alumnos | Bruno, Pepe, Alfonso, Pablo, Antonio | Catálogo, aula, entregas, agenda y resultados |

Responsable de equipo: A pendiente · B Pepe. Responsable de datos: A Adrián · B Bruno.

## Tecnologías

- Python 3.13, Flask (blueprints y application factory)
- SQLAlchemy + PyMySQL sobre MariaDB
- Flask-Login (sesiones) y Flask-WTF (formularios y CSRF)
- Bootstrap 5 e iconos de Bootstrap (CDN)
- pytest y ruff
- Docker y GitHub Actions

Basado en el proyecto *Listo*, ejemplo de la asignatura.

## Organización

- **Work Items:** GitHub Issues con una plantilla común. Cada persona tiene WIs propios.
- **Tablero:** GitHub Projects.
- **Estados de un WI:** Pendiente → Preparado → En curso → En revisión → Terminado.
- **Tipos:** Funcionalidad, Error, Tarea técnica, Documentación.
- **Prioridad:** P0 (bloquea) · P1 (necesario para el MVP) · P2 (mejora) · P3 (futuro).
- **Revisión:** otra persona comprueba cada WI y lo deja anotado en el propio WI. No hay PRs dentro de un mismo equipo.

### Ramas

| Rama | Uso |
| --- | --- |
| `main` | Solo entregas |
| `trunk` | Integración principal |
| `team/a`, `team/b` | Rama de cada equipo |
| `feature/x` | Una funcionalidad |
| `bugfixes` | Corrección de errores |

Las PRs solo se admiten entre equipos y deben estar justificadas.

### Commits

Formato `tipo(ámbito): descripción (#WI)`. Cada persona usa siempre el mismo nombre de autor y hace los commits en local, nunca desde la web de GitHub.

```text
feat(entregas): permite editar antes del cierre (#32)
fix(evaluacion): rechaza notas superiores a diez (#47)
test(permisos): comprueba acceso a entregas ajenas (#51)
docs(producto): concreta los estados de inscripción (#12)
ci(pruebas): ejecuta la integración con MariaDB (#15)
build(docker): prepara la imagen de la aplicación (#18)
```

No se versionan `.env`, credenciales ni configuración de IDE.

### Integración continua

GitHub Actions ejecuta `python scripts/build.py` con cada push:

1. Valida archivos y configuración sin imprimir secretos.
2. Comprueba que `TEST_DB_NAME` es una base de pruebas distinta de la normal.
3. Prepara solo esa base aislada.
4. Ejecuta pytest (unitarias, integración y ciclo completo).
5. Construye la imagen Docker.
6. Devuelve 0 únicamente si todo ha ido bien.

Cada tarea debe incluir sus tests, su WI y commits atómicos. Se valorará más la organización que el resultado final.

## Funcionalidades

El orden de la tabla es el orden de desarrollo. Antes de empezar, se cierran la documentación y las decisiones.

| # | Funcionalidad | Encargado/s | Equipo | Estado |
| --- | --- | --- | --- | --- |
| 1 | Modelado de la base de datos | Bruno y Adrián | Común | Pendiente |
| 2 | Autenticación | Pepe | Común | Pendiente |
| 3 | Asignaturas e inscripciones | José Ángel | A | Pendiente |
| 4 | Catálogo y solicitud | Antonio | B | Pendiente |
| 5 | Materiales | Vicente | A | Pendiente |
| 6 | Actividades | Rodrigo | A | Pendiente |
| 7 | Entrega | Pepe | B | Pendiente |
| 8 | Evaluación | Lucas | A | Pendiente |
| 9 | Aula del alumno | Antonio y Bruno | B | Pendiente |
| 10 | Agenda | Alfonso | B | Pendiente |
| 11 | Resultados | Pablo | B | Pendiente |

Fuera del MVP: media por asignatura o nota final, calendario mensual, chat, pagos, exámenes automáticos, notificaciones e inicio de sesión institucional.

## Criterios de aceptación

**1. Autenticación.** *Como usuario, quiero acceder con mi cuenta.*
- El registro permite crear cuentas de alumnos o profesor y rechaza correos duplicados y campos inválidos.
- Contraseña incorrecta no inicia sesión; cerrar sesión bloquea las páginas privadas.
- Las rutas protegidas comprueban rol e identidad en el servidor.

**3. Asignaturas.** *Como profesor, quiero organizar mis asignaturas y aceptar alumnos.*
- Crear asignatura con código único, nombre, descripción y curso académico.
- Solo edito las mías.
- Veo las solicitudes pendientes y las acepto o rechazo; una decisión repetida o ajena no cambia nada.
- Aceptar da acceso al aula; rechazar no.

**4. Catálogo y solicitud.** *Como alumno, quiero explorar asignaturas y solicitar acceso.*
- El catálogo público solo muestra información pública.
- La solicitud queda asociada al alumno de la sesión y empieza pendiente; no se duplica.
- Veo mi estado: pendiente, aceptada o rechazada.

**5. Materiales.** *Como profesor, quiero publicar materiales.*
- Crear, consultar, editar y eliminar materiales de mis asignaturas.
- Título y contenido obligatorios; enlace opcional (solo HTTP o HTTPS).
- Un alumno aceptado los ve; un visitante o alumno no aceptado no puede abrirlos ni por URL directa.

**6. Actividades.** *Como profesor, quiero publicar instrucciones y una fecha límite.*
- La actividad aparece en el aula y la agenda del alumno.
- El servidor rechaza cierres pasados y campos vacíos.
- No puedo tocar actividades de otro profesor.
- Se puede editar o eliminar solo mientras no tenga entregas.

**7. Entrega.** *Como alumno, quiero entregar y poder editar antes del cierre.*
- Solo entrego en asignaturas donde estoy aceptado.
- El servidor rechaza texto vacío, entregas ajenas y peticiones fuera de plazo.
- Una única entrega por alumno y actividad, incluso con envíos repetidos.
- La confirmación muestra fecha y hora de la última modificación.

**8. Evaluación.** *Como profesor, quiero devolver nota y comentarios.*
- Veo los alumnos aceptados y quién ha entregado.
- Solo evalúo entregas de mis asignaturas y solo desde el cierre.
- Nota de 0 a 10 y comentario no vacío.
- Guardar o corregir actualiza el resultado del alumno.

**9. Aula del alumno.** *Como alumno, quiero ver mis asignaturas y su contenido en un solo sitio.*
- «Mis asignaturas» muestra las aceptadas; las solicitudes se ven aparte.
- Cada aula ofrece materiales y actividades; los estados vacíos lo explican.
- Un alumno ajeno no entra ni por identificador.
- Funciona en móvil y con teclado.

**10. Agenda.** *Como alumno, quiero consultar mis fechas límite.*
- Actividades de mis asignaturas aceptadas, ordenadas por cierre, con filtro por asignatura y fechas.
- Estado en texto: pendiente, vencida sin entrega, entregada o evaluada.
- El profesor tiene una vista equivalente de sus actividades.

**11. Resultados.** *Como alumno, quiero ver mis notas y lo que tengo pendiente.*
- Solo veo mis notas y comentarios.
- Entregada y sin corregir: «Pendiente de evaluación».
- El resumen separa pendientes, vencidas, entregadas y evaluadas; no hay nota final inventada.

## Reglas de negocio

- El correo es único (sin espacios ni mayúsculas) y las contraseñas se guardan con hash.
- Una asignatura tiene un solo profesor responsable.
- Una inscripción por alumno y asignatura. Pendiente o rechazada no da acceso al contenido.
- Materiales y actividades se publican al instante (sin borradores).
- Se entrega solo mientras la hora del servidor sea anterior al cierre; no hay entregas tardías.
- Se evalúa desde el cierre; la evaluación se puede corregir, sin historial.
- Una actividad con entregas ya no se edita ni se elimina.
- No se borran usuarios, asignaturas ni inscripciones desde la interfaz.
- Fechas guardadas en UTC y mostradas en hora de Madrid.
- Los permisos se comprueban en el servidor en cada operación.

## Decisiones pendientes

- **Alta de profesores:** el registro público solo crea alumnos. Para la demo, ¿se permite también registrar profesores?
- **Archivos adjuntos:** tipo, tamaño y almacenamiento privado. Propuesta: empezar con entrega de texto y dejar el archivo como ampliación.
- **Rechazadas:** ¿puede un alumno volver a solicitar tras un rechazo?
- **Media:** queda fuera del MVP, salvo que se defina su cálculo.

Las demás reglas (bloqueo de actividades con entregas, evaluación solo tras el cierre, hora de Madrid y comportamiento exacto al cierre) se dan por cerradas.

## Ejecución prevista

**Local** (necesita MariaDB vacía y un `.env` copiado de `.env.example`; no se versiona):

```bash
python3.13 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
flask --app etsii_learn db-upgrade
flask --app etsii_learn seed-demo
flask --app etsii_learn run --debug   # http://127.0.0.1:5000
```

**Docker:**

```bash
docker compose up --build -d
docker compose exec web flask --app etsii_learn db-upgrade
docker compose exec web flask --app etsii_learn seed-demo
docker compose down
```

**Verificación:** `python scripts/build.py`

## Documentación

| Documento | Contenido |
| --- | --- |
| [Mínimos para aprobar](docs/minimos.md) | Requisitos del enunciado |
| [Arquitectura](docs/arquitectura.md) | Stack, estructura de carpetas, CI y Docker |
| [Datos](docs/datos.md) | Tablas, relaciones y permisos por rol |
| [Diseño](docs/diseno.md) | Colores, botones, estados, navegación y textos comunes |