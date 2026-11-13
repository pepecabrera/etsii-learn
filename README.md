# ETSII Learn

Plataforma educativa para organizar la docencia, las entregas y la evaluación de asignaturas en el contexto de la ETSII de la Universidad de Sevilla.

**Estado: documentación inicial; aplicación pendiente de implementación.** Este paquete contiene el plan del proyecto. No incluye todavía código ejecutable, base de datos, contenedores ni pruebas implementadas. Los comandos de ejecución de este README son convenciones que deberán hacerse funcionar durante el primer hito.

Versión documental: 0.1 · Fecha: 13 de noviembre de 2026 · Equipo: dos grupos de cinco personas · Plan de referencia: seis semanas.

## Objetivo

Completar desde una misma aplicación el recorrido: un profesor publica una actividad, un alumno inscrito entrega su trabajo, el profesor devuelve comentarios y calificación, y el alumno consulta el resultado.

El catálogo de asignaturas será público. Los materiales, actividades, entregas y calificaciones serán privados. Este es un proyecto académico de estudiantes; no implica un servicio oficial ni una integración autorizada con sistemas de la Universidad.

## Primera versión

| Perfil | Funciones |
| --- | --- |
| Visitante sin cuenta | Consultar catálogo y descripción pública de asignaturas. |
| Alumno | Registrarse, acceder, solicitar inscripción, consultar su aula, entregar texto, ver su agenda y consultar resultados. |
| Profesor | Acceder, gestionar sus asignaturas e inscripciones, publicar materiales y actividades y evaluar entregas. |

Se propone una cuenta con un único rol, un profesor responsable por asignatura, una entrega editable por alumno y actividad hasta el cierre y evaluación de 0 a 10 después del cierre. Son decisiones iniciales de diseño, revisables mediante WIs antes de implementar los módulos afectados.

Las clases particulares, el chat, los pagos, los exámenes automáticos, las notas finales ponderadas, las notificaciones externas y el acceso institucional quedan fuera del MVP. Los archivos adjuntos son una ampliación condicionada a completar antes el ciclo principal.

## Documentación

| Documento | Uso |
| --- | --- |
| [Producto y requisitos](docs/producto.md) | Alcance, reglas, diez historias y criterios de aceptación. |
| [Organización](docs/organizacion.md) | Reparto, WIs, coordinación, revisiones y reglas de Git. |
| [Arquitectura](docs/arquitectura.md) | Stack, módulos, configuración, estructura y construcción. |
| [Datos e integración](docs/datos-e-integracion.md) | Entidades, permisos, estados e interfaces entre equipos. |
| [Diseño](docs/diseno.md) | Paleta, componentes, navegación y bocetos funcionales. |
| [Roadmap y calidad](docs/roadmap-y-calidad.md) | Hitos, pruebas, riesgos y evidencias de evaluación. |

## Reparto

- **Equipo A, gestión docente:** autenticación común, asignaturas, inscripción, materiales, actividades y evaluación.
- **Equipo B, experiencia del alumno:** catálogo, solicitud de inscripción, aula del alumno, entregas, agenda y resultados.
- **Trabajo compartido:** esquema inicial, navegación, contratos, CI, Docker e integración.

La responsabilidad de un módulo incluye interfaz, lógica, acceso a datos y pruebas. Cada persona mantiene WIs y commits propios. Los códigos A1–A5 y B1–B5 se sustituirán por nombres reales en el documento de organización.

## Preparación del entorno

Propuesta técnica: Python 3.12, Flask 3.1, MariaDB 11.4, Jinja, HTML, CSS y JavaScript sin framework de frontend. Las versiones exactas de parche se fijarán tras comprobar la primera instalación en Windows y macOS.

Antes de utilizar los comandos siguientes, deben existir los archivos y comandos de gestión descritos en [Arquitectura](docs/arquitectura.md). Actualmente no están implementados.

### Instalación local prevista

1. Clonar el único repositorio entregable; su URL está pendiente.
2. Crear y activar un entorno virtual.

Windows, PowerShell:

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

macOS o Linux:

~~~bash
python3.12 -m venv .venv
source .venv/bin/activate
~~~

3. Instalar las dependencias cuando exista el fichero correspondiente:

~~~bash
python -m pip install -r requirements-dev.txt
~~~

4. Copiar el futuro archivo .env.example a .env, establecer valores locales y preparar una base MariaDB vacía. No versionar .env.
5. Aplicar el esquema y crear datos ficticios mediante los futuros comandos:

~~~bash
flask --app etsii_learn db-upgrade
flask --app etsii_learn seed-demo
flask --app etsii_learn run --debug
~~~

Dirección local prevista: http://127.0.0.1:5000. El modo debug se limita al desarrollo local. Las contraseñas de demostración se introducirán localmente o se generarán; no se guardarán credenciales en el repositorio.

### Ejecución en contenedores prevista

Cuando estén implementados Dockerfile y compose.yaml:

~~~bash
docker compose up --build -d
docker compose exec web flask --app etsii_learn db-upgrade
docker compose exec web flask --app etsii_learn seed-demo
docker compose logs web
docker compose down
~~~

Los servicios previstos se llaman web y db. La base persistirá en un volumen. Detener los contenedores no debe borrar ese volumen. La inicialización no se ejecutará sobre bases de datos ajenas.

### Verificación prevista

~~~bash
python scripts/build.py
~~~

El script deberá validar la configuración, ejecutar pruebas con una base de datos aislada y construir la imagen. Debe devolver un código distinto de cero si falla una etapa. CI lo ejecutará desde el repositorio con cada push.

## Primeros pasos del equipo

1. Sustituir los diez códigos de persona por nombres e identidades Git estables.
2. Confirmar la fecha de entrega y las horas disponibles.
3. Incorporar el modelo de ramas y los commits obligatorios que indique la asignatura.
4. Revisar las reglas del MVP y asignar las diez historias en el tablero.
5. Construir una base común y demostrar acceso a MariaDB desde Flask.
6. Integrar una actividad creada por el profesor y consultada por un alumno autorizado.

No se considera terminado un módulo hasta verificar su conexión con el resto del sistema.
