# ETSII Learn · Organización y colaboración

Versión 0.1 · 13 de noviembre de 2026.

## 1. Principios

Un repositorio entregable, dos equipos de cinco personas y un producto integrado. Cada persona participa en funcionalidad, revisión y pruebas. La documentación, Docker o la coordinación no sustituyen una contribución funcional.

Los WIs serán la fuente del estado del trabajo. Las decisiones de producto y arquitectura se consolidarán en estos documentos. El chat sirve para coordinar, no para mantener acuerdos que solo conocen dos personas.

## 2. Responsabilidades por persona

Los nombres y usuarios se completarán antes del primer desarrollo. Cada fila corresponde a una persona, no a una cuenta compartida.

| Código | Nombre / autor Git | Funcionalidad principal | Apoyo transversal inicial |
| --- | --- | --- | --- |
| A1 | Pendiente | Autenticación, registro y roles | Configuración común y permisos |
| A2 | Pendiente | Asignaturas y decisiones de inscripción | Esquema y contratos de acceso al aula |
| A3 | Pendiente | Gestión de materiales | Componentes docentes |
| A4 | Pendiente | Actividades y plazos | Integración con agenda y entregas |
| A5 | Pendiente | Revisión y evaluación | Datos de demostración docente |
| B1 | Pendiente | Catálogo y solicitudes de inscripción | Pruebas de integración y respaldo de CI |
| B2 | Pendiente | Mis asignaturas y aula del alumno | Diseño común y navegación |
| B3 | Pendiente | Entregas | CI y script de construcción |
| B4 | Pendiente | Agenda de ambos perfiles | Docker, con A1 de respaldo |
| B5 | Pendiente | Resultados y seguimiento | Guion de aceptación y documentación de uso |

Son apoyos propuestos, revisables según conocimientos y carga. La creación de interfaces compartidas es trabajo conjunto. A1 no debe convertirse en la única persona capaz de arrancar el proyecto.

Cada equipo nombrará un enlace de integración y un sustituto. No se asignan todavía nombres. Los enlaces resuelven dependencias y comunican cambios; no centralizan los commits del grupo.

## 3. Propiedad de módulos y datos

| Área | Responsable principal | Consumidores |
| --- | --- | --- |
| Autenticación y contexto de usuario | A1 | Todos |
| Asignaturas e inscripciones | A2 | B1, B2 y módulos privados |
| Materiales | A3 | B2 |
| Actividades | A4 | A5, B2, B3, B4 y B5 |
| Entregas | B3 | A5, B4 y B5 |
| Evaluaciones | A5 | B4 y B5 |
| Base visual | A3 y B2 | Todos |
| CI y construcción | B3; respaldo B1 | Todos |
| Docker y entorno | B4; respaldo A1 | Todos |

No se escribirá desde otro módulo en una tabla ajena para evitar una interfaz todavía no implementada. Se acuerda antes el contrato o se abre un WI compartido. Las consultas de lectura agregadas para agenda se acuerdan con los propietarios.

## 4. Herramientas

| Necesidad | Propuesta | Regla |
| --- | --- | --- |
| Código | Un repositorio GitHub | URL pendiente; todo el historial debe conservarse. |
| WIs | GitHub Issues | Una plantilla común; cada persona tiene WIs propios. |
| Tablero | GitHub Projects | Vistas por equipo, responsable, estado e hito. |
| CI | GitHub Actions | Se activa con push; no depende de PRs internos. |
| Comunicación | WhatsApp | Discord o Teams son otras opciones. |
| Bocetos | Penpot, Figma o draw.io | Decisiones y capturas aprobadas se incorporan al repositorio. |
| Documentos | Markdown en docs | No mantener versiones definitivas contradictorias en varios servicios. |

## 5. Proceso de Work Items

### Tipos y prioridad

| Tipo | Uso |
| --- | --- |
| Funcionalidad | Comportamiento para un usuario. |
| Error | Comportamiento que incumple lo acordado. |
| Tarea técnica | Base de datos, CI, Docker, refactorización o integración. |
| Documentación | Acuerdos, instalación, diseño o evidencias. |

| Prioridad | Significado |
| --- | --- |
| P0 | Bloquea a varios miembros, rompe el ciclo principal o expone datos privados. |
| P1 | Necesario para el MVP o la evaluación de la asignatura. |
| P2 | Mejora prevista tras completar el núcleo. |
| P3 | Idea futura sin compromiso en la entrega actual. |

### Estados

| Estado | Condición |
| --- | --- |
| Pendiente | Idea o trabajo registrado que aún necesita detalle. |
| Preparado | Objetivo, criterios, dependencias, prioridad y responsable definidos. |
| En curso | El responsable ha empezado; se enlazan avances y commits. |
| En revisión | Implementación y pruebas listas para comprobación por otra persona. |
| Terminado | Criterios cumplidos, revisión registrada, pruebas correctas e integración comprobada. |

Un bloqueo se registra como etiqueta o campo adicional, con motivo, persona que debe resolverlo y siguiente acción. El WI mantiene su estado real. Reabrirlo es válido si la revisión detecta un fallo.

### Roles

- **Solicitante:** explica la necesidad; puede ser el propio responsable.
- **Responsable:** mantiene el WI y desarrolla el cambio.
- **Revisor:** otra persona comprueba criterios, permisos y pruebas.
- **Enlace de integración:** interviene cuando hay impacto entre equipos.

Cada persona tendrá normalmente un WI en curso. Los WIs grandes se dividen; como orientación, una unidad debería poder revisarse tras uno o dos días de trabajo efectivo.

### Plantilla común para copiar a GitHub

El siguiente bloque es contenido de una plantilla; todavía no se ha instalado un formulario de Issues en el repositorio.

~~~markdown
## Objetivo
Como [perfil], quiero [acción] para [beneficio].

## Clasificación
- Tipo:
- Prioridad:
- Equipo:
- Responsable:
- Revisor:
- Hito:
- Historia relacionada:

## Alcance
Comportamiento que incluye este WI y límites relevantes.

## Criterios de aceptación
- [ ] Resultado observable 1.
- [ ] Validación o permiso relevante.
- [ ] Comportamiento ante error o estado vacío.

## Dependencias e integración
WIs previos, módulo afectado, contrato utilizado y cambio de esquema si existe.

## Verificación
Pasos o prueba automática que demuestra los criterios.

## Evidencias al cerrar
Commits, resultado de pruebas, revisión e integración comprobada.
~~~

Instalar esta plantilla como formulario versionado es una tarea de la semana 1. Las plantillas, workflows y documentación también se crean y modifican con commits locales.

## 6. Backlog inicial

| Referencia | Responsable | Prioridad | Dependencias |
| --- | --- | --- | --- |
| HU-A1 | A1 | P1 | Base común |
| HU-A2 | A2 | P1 | HU-A1 |
| HU-A3 | A3 | P1 | HU-A2 |
| HU-A4 | A4 | P1 | HU-A2 |
| HU-A5 | A5 | P1 | HU-A4 y HU-B3 |
| HU-B1 | B1 | P1 | Consulta pública de asignaturas y servicio de inscripción |
| HU-B2 | B2 | P1 | HU-A2, HU-A3 y HU-A4 |
| HU-B3 | B3 | P1 | HU-A1, HU-A2 y HU-A4 |
| HU-B4 | B4 | P1 | HU-A4 y contratos de entrega y evaluación |
| HU-B5 | B5 | P1 | HU-B3 y HU-A5 |

Añadir WIs técnicos para esquema, entorno, contratos, plantilla, CI, construcción y Docker. Asignarlos explícitamente y estimarlos junto a las historias funcionales.

## 7. Revisión sin PRs dentro del equipo

1. El autor prepara un cambio pequeño con pruebas y lo vincula a un WI.
2. Otra persona comprueba el diff, ejecuta el caso y revisa criterios y permisos.
3. El revisor registra qué comprobó en el WI y qué commit revisó.
4. El autor corrige si procede y realiza la integración mediante el flujo local acordado.
5. Se comprueba el resultado integrado y se cierra el WI.

Una revisión verbal sin constancia no aporta la misma evidencia. No es necesario abrir una PR para realizar estos pasos.

## 8. Git y autoría

### Reglas confirmadas por el enunciado

- Un repositorio final conserva toda la historia del proyecto.
- No hay PRs dentro de un mismo equipo.
- Las PRs entre equipos deben estar justificadas.
- Los commits se hacen localmente y después se sincronizan.
- Cada una de las diez personas mantiene una identidad de autor estable.
- Debe existir un patrón homogéneo de commits y participación equilibrada.
- No se versionan secretos, configuración de IDE ni archivos ajenos al proyecto.
- El modelo de uso del repositorio enseñado en clase tiene prioridad.

### Modelo de ramas pendiente

No se fija una estrategia definitiva porque aún no se dispone del modelo docente. Antes del primer cambio paralelo se documentarán aquí:

| Decisión | Valor |
| --- | --- |
| Rama entregable y rama de integración, si existe | Pendiente del modelo de clase |
| Ramas de equipo o funcionalidad | Pendiente del modelo de clase |
| Forma de integrar cambios dentro del equipo | Fusiones locales según modelo confirmado |
| Forma de integrar cambios entre equipos | Según modelo confirmado; PR si corresponde y está justificada |
| Commits y etiquetas obligatorios | Pendiente del enunciado completo |

Puede reducirse el número de PRs entre equipos agrupando incrementos coherentes, pero no se pospone la primera integración a la entrega final. No se impondrá una protección de rama que obligue a PRs prohibidos por el enunciado.

### Identidad estable

Cada persona configura en el repositorio local su nombre de autor y un correo asociado a su cuenta. Los valores siguientes son ejemplos para sustituir, no identidades comunes para copiar entre personas:

~~~bash
git config user.name "Nombre Apellido de esta persona"
git config user.email "correo-propio-asociado-a-github"
git log --format="%an <%ae>" --all
~~~

Mantener el mismo nombre en Windows, macOS y cualquier otro equipo. No utilizar una cuenta compartida ni hacer todos los commits desde el ordenador del enlace.

### Patrón de commits

Formato: tipo(ámbito): descripción breve, con referencia al WI real cuando exista.

~~~text
feat(entregas): permite editar antes del cierre (#32)
fix(evaluacion): rechaza notas superiores a diez (#47)
test(permisos): comprueba acceso a entregas ajenas (#51)
docs(producto): concreta los estados de inscripción (#12)
ci(pruebas): ejecuta la integración con MariaDB (#15)
build(docker): prepara la imagen de la aplicación (#18)
~~~

Los números son ilustrativos. No dividir artificialmente cambios para aumentar el contador ni reunir trabajo de varias personas bajo un solo autor. No reescribir historia compartida como procedimiento habitual.

### Archivos excluidos

Preparar un .gitignore que excluya al menos .env, .venv, __pycache__, .pytest_cache, credenciales, volcados privados, volúmenes locales, .DS_Store, .idea y .vscode. Mantener .env.example con nombres y valores de ejemplo no sensibles. Las plantillas de Issues y workflows sí pertenecen a Git.

## 9. Cadencia

- Inicio de semana: 20–30 minutos por equipo para priorizar y detectar dependencias.
- Durante la semana: comunicación breve si cambia un contrato o aparece un bloqueo.
- Una vez por semana: demostración conjunta de 30–45 minutos, con un recorrido integrado y revisión de CI.
- Cierre de semana: actualizar WIs, riesgos y decisiones. Comparar carga y contribución para redistribuir trabajo real.

## 10. Gestión de cambios compartidos

Antes de modificar una relación, firma de servicio, permiso, componente común o archivo de arranque:

1. Abrir un WI con el motivo, consumidores afectados y alternativa propuesta.
2. Acordar el cambio con el otro equipo.
3. Actualizar contrato, implementación y pruebas de sus consumidores.
4. Integrar mediante el modelo Git confirmado y comprobar el ciclo afectado.

Una decisión pendiente no implica pedir autorización para cada detalle de implementación. El equipo responsable resuelve los detalles locales que no cambian el comportamiento acordado.
