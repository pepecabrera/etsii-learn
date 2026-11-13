# ETSII Learn · Roadmap, calidad y entrega

Versión 0.1 · 13 de noviembre de 2026 · Horizonte de referencia: seis semanas.

**Estado inicial:** planificación. Ninguna prueba, instalación, integración o ejecución de CI se considera realizada por la existencia de este documento.

## 1. Calendario y capacidad

La disponibilidad declarada es de uno a dos meses. El plan se expresa por semanas relativas porque no se ha confirmado una fecha de entrega.

| Dato | Valor |
| --- | --- |
| Inicio real | Pendiente |
| Entrega final | Pendiente |
| Horas semanales por persona | Pendiente |
| Integrantes | Diez, repartidos en dos equipos |
| Plan de referencia | Seis semanas |

Estimar los WIs cuando se conozcan las horas disponibles. No suponer dedicación a tiempo completo. Reservar la última semana del plan de seis semanas para estabilización y entrega, manteniendo integración desde las primeras semanas.

## 2. Hitos y criterios de salida

| Hito | Semana | Resultado | Evidencia para terminarlo |
| --- | --- | --- | --- |
| H0 · Acuerdos | Inicio de 1 | Alcance, reparto, reglas, Git docente y tablero definidos | Documentos revisados, diez personas identificadas y WIs preparados |
| H1 · Base ejecutable | 1 | Flask, MariaDB, acceso básico, CI y Docker | Instalación local y Compose reproducibles, una prueba real y workflow ejecutado |
| H2 · Aula y acceso | 2 | Profesor crea asignatura; alumno solicita y recibe acceso | Solicitud aceptada y rechazada con permisos comprobados |
| H3 · Publicación integrada | 3 | Material y actividad creados por profesor aparecen al alumno autorizado | Recorrido real entre ambos módulos y agenda inicial |
| H4 · Ciclo completo | 4 | Entrega, evaluación y consulta del resultado | Prueba integrada con MariaDB y demostración de ambos perfiles |
| H5 · Consolidación | 5 | Agenda, seguimiento, validaciones y permisos completos | Pruebas críticas correctas y revisión visual de ambos perfiles |
| H6 · Entrega | 6 | Versión reproducible y documentación actualizada | Arranque desde cero, CI correcta y guion de demostración ensayado |

Si una semana termina con su criterio pendiente, registrar el desvío y ajustar alcance. No declarar un hito terminado porque las pantallas existan de forma aislada.

## 3. Trabajo en paralelo

| Semana | Equipo A | Equipo B | Trabajo compartido |
| --- | --- | --- | --- |
| 1 | Autenticación, esquema de asignaturas y base docente | Navegación, catálogo inicial, CI y Docker | Modelo de datos, contratos, estilos y entorno |
| 2 | Asignaturas, decisiones de inscripción y primeros materiales | Solicitudes, mis asignaturas y base de entregas | Primera comprobación de acceso privado |
| 3 | Actividades y consulta docente de trabajos | Aula, entrega de texto y agenda | Publicación visible y contrato de entregas |
| 4 | Evaluación y corrección de permisos | Consulta de resultados y resumen | Recorrido completo y pruebas automáticas |
| 5 | Validaciones y errores docentes | Agenda, estados y adaptación móvil | Pruebas de concurrencia, revisión y documentación |
| 6 | Correcciones y preparación de demo | Correcciones y preparación de demo | Instalación desde cero y entrega |

Los contratos permiten preparar un consumidor antes de que termine el productor. Un consumidor con datos simulados no se considera integrado hasta conectarlo al productor real.

### Adaptación a cuatro semanas

Conservar catálogo, inscripción, materiales de texto, actividad, entrega de texto, evaluación, listado de fechas y requisitos técnicos. Reducir refinamientos visuales, filtros secundarios y amplitud de los paneles. Integrar publicación en la semana 2 y el ciclo completo en la 3. Reservar la 4 para estabilizar.

Si la capacidad sigue siendo insuficiente, revisar el alcance con los tutores; no eliminar CI, Docker o la integración para mantener una función opcional.

### Adaptación a ocho semanas

Usar el margen para reforzar pruebas, corregir usabilidad e incorporar adjuntos privados si se aprueba ese WI. No añadir chat o clases particulares antes de verificar los dos perfiles y el ciclo completo.

## 4. Dependencias críticas

1. Autenticación común habilita las funciones privadas.
2. Asignaturas e inscripciones habilitan el aula.
3. Actividades habilitan agenda y entregas.
4. Entregas habilitan evaluación.
5. Evaluación habilita los resultados reales del alumno.

Los contratos, configuración, esquema y estilos son trabajo de la primera semana. CI y Docker se desarrollan en paralelo al primer módulo.

## 5. Definición de preparado y terminado

Un WI está **preparado** cuando tiene responsable, prioridad, objetivo, criterios de aceptación verificables, dependencias e impacto en datos o contratos.

Un WI está **terminado** cuando:

- Cumple sus criterios y el comportamiento se puede reproducir.
- Verifica permisos y errores relevantes.
- Tiene pruebas proporcionales al cambio.
- Ha sido revisado por otra persona y queda constancia en el WI.
- Sus commits se enlazan y utilizan el patrón común.
- Está integrado y se ha comprobado el consumidor afectado.
- La CI aplicable está correcta y la documentación necesaria está actualizada.

No escribir pruebas que solo repliquen el código. Priorizar reglas, aislamiento de usuarios y recorridos que pueden romper la aplicación.

## 6. Estrategia de pruebas

| Nivel | Uso | Entorno |
| --- | --- | --- |
| Unitarias | Fechas, estados derivados y validaciones aislables | Reloj controlado y sin servicios externos |
| Integración | Rutas Flask, permisos, SQL, restricciones y transacciones | MariaDB de pruebas real |
| Aceptación automatizada | Recorrido entre los módulos de ambos equipos | Cliente de pruebas de Flask y MariaDB |
| Revisión manual | Navegación, móvil, teclado, mensajes y presentación | Navegador |
| Construcción y despliegue | Imagen, configuración, migraciones y arranque | Local y Docker Compose |

No utilizar SQLite como sustituto de la integración con MariaDB. Las pruebas de aceptación con el cliente Flask verifican rutas y datos; no sustituyen revisar el funcionamiento visual y JavaScript en navegador.

Cada ejecución utiliza una base aislada. Nunca ejecutar limpieza o fixtures sobre la base de demostración o sobre datos personales.

## 7. Catálogo mínimo de comprobaciones planificadas

Todas parten como pendientes. Sus identificadores sirven para nombrar pruebas y relacionarlas con WIs.

| ID | Comprobación | Responsable inicial |
| --- | --- | --- |
| T01 | Registro correcto, correo duplicado y rol de profesor manipulado | A1 |
| T02 | Acceso válido, contraseña incorrecta y cierre de sesión | A1 |
| T03 | Protección de rutas privadas y CSRF en escrituras | A1 con autores de rutas |
| T04 | Profesor ajeno no modifica una asignatura | A2 |
| T05 | Solicitud única y estados pendiente, aceptada y rechazada | A2 y B1 |
| T06 | Visitante o alumno no aceptado no lee materiales ni actividades | A2, A3 y B2 |
| T07 | Material actualizado visible y enlace con esquema inválido rechazado | A3 |
| T08 | Actividad con título vacío o cierre pasado rechazada | A4 |
| T09 | Actividad sin entregas editable y con entregas bloqueada | A4 y B3 |
| T10 | Alumno aceptado entrega texto y consulta lo guardado | B3 |
| T11 | Entrega vacía, demasiado grande o de alumno ajeno rechazada | B3 |
| T12 | Edición permitida antes del cierre y rechazada exactamente en el cierre | B3 |
| T13 | Dos envíos simultáneos no crean entregas duplicadas | B3 |
| T14 | Edición de actividad y primera entrega concurrentes mantienen las reglas | A4 y B3 |
| T15 | No se permite corregir antes del cierre | A5 |
| T16 | Notas 0 y 10 válidas; fuera de rango y comentario vacío rechazados | A5 |
| T17 | Otro profesor no consulta ni evalúa trabajos ajenos | A5 |
| T18 | Alumno ajeno no consulta entrega ni evaluación | A5 y B5 |
| T19 | Editar una evaluación actualiza la pantalla del alumno | A5 y B5 |
| T20 | Agenda solo incluye asignaturas accesibles y respeta filtros | B4 |
| T21 | Estados pendiente, vencida, entregada y evaluada coherentes | B4 y B5 |
| T22 | Fechas UTC y presentación Madrid, incluidos cambios de horario | A4 y B4 |
| T23 | Contenido con HTML se muestra como texto, sin ejecutar scripts | A3 y B3 |
| T24 | Error de base de datos no deja una operación parcialmente guardada | Autores de servicios |
| T25 | Ciclo publicación → entrega → evaluación → resultado | Ambos enlaces |
| T26 | Instalación local desde una copia limpia siguiendo README | Una persona de cada sistema operativo |
| T27 | Compose arranca, migraciones aplican y datos persisten tras reiniciar | B4 y A1 |
| T28 | Script falla si falla una prueba y protege la base normal | B3 y B1 |
| T29 | CI se ejecuta con push y muestra el resultado de pruebas y build | B3 |
| T30 | Navegación con teclado, móvil y zoom al 200 % | A3 y B2 |

Las pruebas concurrentes deben coordinar las operaciones con conexiones separadas; repetir peticiones secuenciales no demuestra concurrencia.

## 8. Evidencias frente a los mínimos docentes

La tabla diferencia obligaciones del enunciado de recomendaciones del proyecto. No presupone requisitos de commits que aún no se han facilitado.

| Mínimo indicado | Evidencia prevista |
| --- | --- |
| Proyecto usable y ciclo completo | T25 y demostración con profesor y alumno |
| Integración real entre subsistemas | Publicación, entrega y resultado con la misma base y cuentas |
| Al menos un WI por miembro | Diez personas con WIs asignados, realizados y revisados |
| Tipos, estados, roles y prioridad de WIs | Tablero, plantilla y reglas de organización utilizadas |
| Plantilla homogénea | Formulario versionado y WIs finales completos |
| Un repositorio entregable e historial | URL única y log de todo el proyecto |
| Sin PRs internas y PRs compartidas justificadas | Registro del flujo y motivo en las PRs entre equipos |
| Identidad estable de cada autor | Revisión periódica de nombres de autor en todo el historial |
| Commits locales y patrón común | Procedimiento acordado y revisión del historial |
| Participación homogénea | Revisión de contribuciones reales y redistribución de carga |
| Commits específicos del enunciado | Checklist pendiente de completar con el enunciado íntegro |
| Sin configuración de IDE ni secretos | .gitignore, .dockerignore y revisión del contenido versionado |
| Modelo Git de clase | Decisión pendiente documentada antes del trabajo paralelo |
| Servidor CI conectado al repositorio | Ejecuciones reales de Actions |
| Script de construcción personalizado | scripts/build.py implementado y utilizado |
| Alguna prueba integrada | Pruebas automáticas ejecutadas por CI |
| Despliegue local | T26, instrucciones actualizadas y demostración |
| Despliegue Docker | T27, Dockerfile y compose.yaml funcionales |

PRD, manual visual y roadmap son documentos recomendados para organizar este proyecto. Sus nombres concretos no aparecen como obligación en el fragmento recibido.

## 9. Riesgos y respuesta

| Riesgo | Señal | Respuesta |
| --- | --- | --- |
| Dependencia de autenticación | Equipo B sin usuario funcional | Base compartida y cuenta ficticia desde H1; contrato temprano |
| Integración tardía | Módulos solo funcionan con datos simulados | Demostración conjunta semanal y consumidores reales |
| Sobrecarga del equipo A | Asignaturas o actividades retrasan a varios | Redistribuir WIs concretos conservando propiedad y acuerdos |
| Alcance creciente | Chat o adjuntos desplazan entregas y evaluación | Mantener P2/P3 hasta H4 |
| Entornos distintos | Funciona solo en un ordenador | Versiones comunes, README y Docker desde H1 |
| Fuga de datos entre alumnos | Acceso mediante un id cambiado | T06, T17 y T18 antes de dar por terminada una ruta |
| Fechas incoherentes | El navegador permite algo que el servidor rechaza sin explicación | UTC, validación de servidor y mensajes coherentes |
| Incumplir reglas Git | PR interna o nombres de autor distintos | Confirmar modelo docente e identidad antes de colaborar |
| Pérdida de tiempo en la demo | La actividad aún no ha cerrado | Dataset coherente con actividad abierta y otra cerrada |

## 10. Guion de demostración

Preparar datos ficticios mediante el futuro seed-demo, con dos profesores y tres alumnos. No incluir contraseñas reales en capturas ni documentos públicos.

1. Abrir catálogo sin sesión y mostrar que el contenido académico está protegido.
2. Acceder como alumno, solicitar acceso y mostrar el estado pendiente.
3. Acceder como profesor responsable y aceptar la solicitud.
4. Publicar material y actividad abierta; mostrar ambos desde el alumno.
5. Entregar texto y comprobar el estado y fecha de guardado.
6. Abrir otra actividad ya cerrada con una entrega anterior al cierre; explicar que se utiliza para no esperar durante la demostración.
7. Evaluar esa entrega y consultar nota y comentario desde el alumno correspondiente.
8. Intentar abrir esa entrega con otro alumno y mostrar la denegación.
9. Mostrar una ejecución correcta de CI y el script de construcción.
10. Demostrar ejecución local y con Docker siguiendo las instrucciones entregadas.

La prueba automatizada T25 debe recorrer publicación, entrega y evaluación de la misma actividad con un reloj controlado. La demostración manual utiliza dos actividades para hacer visible el mismo comportamiento sin alterar el reloj del sistema.

## 11. Checklist final

- [ ] Fecha, nombres y modelo Git docente completados.
- [ ] Funciones P1 implementadas y comprobadas.
- [ ] Cada persona tiene WIs y commits propios con identidad estable.
- [ ] WIs finales usan la plantilla y tienen evidencia de revisión.
- [ ] Pruebas críticas y CI correctas sobre la versión integrada.
- [ ] Script de construcción propio y Docker funcionales.
- [ ] README contrastado desde una copia limpia en local y contenedores.
- [ ] Sin credenciales, configuraciones de IDE ni datos privados en Git.
- [ ] Decisiones de producto, contratos y esquema reflejan la versión final.
- [ ] Dataset ficticio y guion ensayados.
- [ ] Incidencias conocidas registradas con impacto y prioridad.
- [ ] Versión final identificada según las reglas de la asignatura.

## 12. Registro de avance

Completar semanalmente; los campos vacíos no significan que se haya realizado una verificación.

| Semana / fecha | Hito real | Evidencia / commit | Bloqueos | Ajuste acordado |
| --- | --- | --- | --- | --- |
| 1 / pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 2 / pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 3 / pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 4 / pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 5 / pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| 6 / pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
