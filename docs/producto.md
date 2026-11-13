# ETSII Learn · Producto y requisitos

Versión 0.1 · 13 de noviembre de 2026 · Referencia funcional del MVP.

## 1. Problema y propósito

ETSII Learn busca reunir la organización docente y el trabajo del alumno en una plataforma vinculada al contexto de la escuela. Su primera versión permitirá gestionar asignaturas, materiales, actividades, entregas y evaluación mediante dos perfiles: profesor y alumno.

La identidad propia del centro se reflejará en el catálogo y el contenido. No se presupone acceso a directorios, matrículas o servicios oficiales. No se pretende reproducir todas las funciones de Blackboard en seis semanas.

## 2. Objetivos verificables

| ID | Objetivo | Cómo se comprueba |
| --- | --- | --- |
| O1 | Completar publicación, entrega y evaluación | Demostración de extremo a extremo con dos cuentas. |
| O2 | Mantener privado el contenido académico | Pruebas de acceso anónimo, no inscrito y usuario ajeno. |
| O3 | Ayudar al alumno a organizarse | Agenda derivada de actividades y resumen de sus entregas. |
| O4 | Ofrecer una experiencia común entre equipos | Navegación, estilos, usuarios y datos compartidos. |
| O5 | Poder instalar y comprobar el sistema | Ejecución local y con Docker, script de construcción y CI. |

No se fijan objetivos de adopción real mientras el producto sea una demostración académica.

## 3. Perfiles y acceso

| Actor | Alcance |
| --- | --- |
| Visitante | Catálogo, nombre del profesor y descripción pública de cada asignatura. No ve alumnos, materiales, actividades ni notas. |
| Alumno | Asignaturas con inscripción aceptada y sus propios trabajos y resultados. |
| Profesor | Contenido, inscripciones, entregas y resultados de las asignaturas de las que es responsable. |

El visitante no tiene un rol persistente. Las cuentas tienen un único rol en el MVP. El registro público solo crea alumnos. Las cuentas de profesor se provisionan mediante un comando de gestión o datos iniciales controlados, sin pantalla de administrador.

## 4. Alcance y prioridad

| Prioridad | Función |
| --- | --- |
| P1, imprescindible | Registro de alumnos, acceso, cierre de sesión y permisos. |
| P1 | Catálogo público y gestión de asignaturas propias. |
| P1 | Solicitud de inscripción y aceptación o rechazo. |
| P1 | Materiales con texto y enlaces. |
| P1 | Actividades publicadas con instrucciones y fecha límite. |
| P1 | Entrega de texto editable antes del cierre. |
| P1 | Evaluación con nota y comentario después del cierre. |
| P1 | Aula del alumno, listado de fechas próximas y resultados. |
| P1 | Pruebas, CI, construcción, ejecución local y Docker. |
| P2, ampliación | Un PDF adjunto por material o entrega, con acceso privado y límites. |
| P2 | Calendario mensual sobre las mismas actividades. |
| P3, futuro | Clases particulares, foro, correo y otras funciones sociales. |

P0 se reserva para incidencias que bloquean el desarrollo o el ciclo principal. Una ampliación no desplaza los requisitos de evaluación de la asignatura.

Fuera del MVP: pagos, videollamadas, chat, evaluación automática, exámenes, múltiples profesores por asignatura, grupos docentes, rúbricas, cálculo de nota final, múltiples intentos históricos, importación de matrículas, recuperación de contraseña por correo e inicio de sesión institucional.

## 5. Reglas de negocio propuestas

Estas reglas concretan decisiones pendientes de detalle. Deben revisarse al iniciar el proyecto y mantenerse sincronizadas con [Datos e integración](datos-e-integracion.md).

| ID | Regla |
| --- | --- |
| RN01 | El correo de cuenta es único tras normalizar espacios externos y mayúsculas. Las contraseñas solo se almacenan como hash. |
| RN02 | Cada asignatura tiene un único profesor responsable. Solo él puede modificarla o gestionar su aula. |
| RN03 | Existe como máximo una inscripción por alumno y asignatura. Empieza pendiente; el profesor decide aceptada o rechazada. |
| RN04 | Una inscripción pendiente o rechazada no da acceso al contenido. Reabrir solicitudes o revocar inscripciones queda fuera del MVP. |
| RN05 | Materiales y actividades se publican de inmediato; no hay borradores ni publicación programada. |
| RN06 | Una actividad nueva necesita título, instrucciones y cierre futuro. Solo admite entregas mientras la hora del servidor sea estrictamente anterior al cierre. |
| RN07 | Existe como máximo una entrega por alumno y actividad. Su autor puede editarla antes del cierre. El texto no puede estar vacío. |
| RN08 | El profesor evalúa después del cierre. Son obligatorios una nota entre 0 y 10, ambos incluidos, y un comentario no vacío. |
| RN09 | La evaluación puede corregirse después del cierre. No se conserva un historial de versiones en el MVP. |
| RN10 | Una actividad puede editarse o eliminarse antes de su primera entrega. Una vez que tenga alguna entrega, se bloquean esas operaciones para evitar cambios de condiciones. |
| RN11 | No se ofrece borrado de usuarios, asignaturas o inscripciones desde la interfaz del MVP. Los materiales sí pueden editarse o eliminarse por su profesor. |
| RN12 | La agenda consulta las actividades de las asignaturas aceptadas; no crea copias de sus fechas. |
| RN13 | La interfaz muestra fechas en Europe/Madrid; se almacenan normalizadas a UTC y el servidor decide si el plazo está abierto. |
| RN14 | Los permisos se verifican en cada operación del servidor. Un identificador enviado por formulario no concede acceso. |

Las reglas RN08 y RN10 reducen cambios conflictivos entre entrega y corrección. Si queréis corregir antes del cierre o ampliar plazos después de recibir trabajos, será necesario un WI que defina el nuevo comportamiento.

## 6. Historias por persona y criterios de aceptación

Los identificadores son referencias de documentación, no números de Issues ya creadas. Cada historia se descompone en WIs estimados y asignados.

### HU-A1 · Acceso y perfiles · Persona A1

Como usuario, quiero acceder con mi cuenta para utilizar las funciones de mi perfil.

- El registro crea alumnos y rechaza correos duplicados y campos inválidos.
- No se puede obtener el rol de profesor manipulando una petición de registro.
- Una cuenta válida accede a su panel; una contraseña incorrecta no inicia sesión.
- Cerrar sesión impide seguir utilizando páginas privadas.
- Las rutas protegidas comprueban el rol y la identidad en el servidor.

### HU-A2 · Asignaturas e inscripciones · Persona A2

Como profesor, quiero organizar mis asignaturas y aceptar alumnos.

- Puedo crear una asignatura con código único, nombre, descripción y curso académico.
- Solo puedo editar las asignaturas de las que soy responsable.
- Consulto solicitudes de mis asignaturas y decido sobre las pendientes.
- Aceptar una solicitud permite al alumno entrar en el aula; rechazarla no.
- Una decisión repetida o una solicitud ajena no produce cambios indebidos.

### HU-A3 · Materiales · Persona A3

Como profesor, quiero publicar materiales para mis alumnos.

- Puedo crear, consultar, editar y eliminar materiales de mis asignaturas.
- El título y el contenido son obligatorios; un enlace adicional es opcional.
- Los enlaces admitidos utilizan HTTP o HTTPS.
- Un alumno aceptado ve el material actualizado.
- Un visitante o alumno no aceptado no puede leerlo accediendo directamente a su URL.

### HU-A4 · Actividades · Persona A4

Como profesor, quiero publicar instrucciones y una fecha límite para recibir trabajos.

- Una actividad válida aparece en el aula del alumno y en su agenda.
- El servidor rechaza cierres pasados y campos vacíos.
- No puedo publicar o editar actividades de otro profesor.
- Puedo editar o eliminar una actividad sin entregas; después de la primera entrega queda bloqueada.
- Los cambios permitidos actualizan las vistas del alumno sin duplicar datos.

### HU-A5 · Evaluación · Persona A5

Como profesor, quiero revisar trabajos y devolver una nota y comentarios.

- Veo el listado de alumnos aceptados, distinguiendo quién tiene entrega.
- Solo puedo abrir y evaluar entregas de mis asignaturas.
- La corrección se habilita a partir del cierre de la actividad.
- Se aceptan 0 y 10; se rechazan notas fuera de rango y comentarios vacíos.
- Guardar o corregir una evaluación actualiza el resultado del alumno.

### HU-B1 · Catálogo y solicitud · Persona B1

Como alumno, quiero explorar asignaturas y solicitar acceso.

- El catálogo público muestra únicamente la información pública acordada.
- Un visitante puede consultar una descripción, pero necesita acceder para solicitar inscripción.
- La solicitud queda asociada al alumno de la sesión y empieza pendiente.
- Una segunda solicitud para la misma asignatura no crea duplicados.
- Veo mi estado: pendiente, aceptada o rechazada.

### HU-B2 · Aula del alumno · Persona B2

Como alumno, quiero consultar mis asignaturas y su contenido desde un mismo lugar.

- «Mis asignaturas» muestra las aceptadas; las solicitudes se consultan por separado.
- Cada aula ofrece materiales y actividades con navegación coherente.
- Los estados vacíos explican que todavía no hay contenido.
- Un alumno ajeno no entra al aula ni consulta elementos por su identificador.
- La pantalla funciona en móvil y con teclado.

### HU-B3 · Entrega · Persona B3

Como alumno, quiero entregar mi trabajo y poder editarlo antes del cierre.

- Solo puedo entregar en actividades de asignaturas donde estoy aceptado.
- El servidor rechaza texto vacío, entregas ajenas y peticiones fuera de plazo.
- Puedo consultar mi entrega guardada y modificarla antes del cierre.
- Existe una única entrega por pareja alumno/actividad, incluso ante envíos repetidos.
- La confirmación muestra fecha y hora de la última modificación.

### HU-B4 · Agenda · Persona B4

Como alumno, quiero consultar fechas límite para organizarme.

- Veo actividades de mis asignaturas aceptadas, ordenadas por cierre.
- Puedo filtrar por asignatura y rango de fechas.
- Distingo pendiente, vencida sin entrega, entregada y evaluada mediante texto.
- La información procede de actividades, entregas y evaluaciones reales.
- El profesor dispone de una vista equivalente para sus propias actividades.

### HU-B5 · Resultados y seguimiento · Persona B5

Como alumno, quiero consultar mis resultados y saber qué tengo pendiente.

- Veo únicamente mis notas y comentarios.
- Una actividad entregada y todavía sin corregir indica «Pendiente de evaluación».
- El resumen diferencia pendientes, vencidas sin entrega, entregadas y evaluadas.
- Corregir una calificación se refleja en mi pantalla.
- No se muestra una nota final de asignatura inventada a partir de medias.

## 7. Requisitos de calidad

- Persistencia en MariaDB; los datos sobreviven a reiniciar la aplicación.
- SQL parametrizado, protección CSRF y escape del contenido mostrado.
- Navegación por teclado, etiquetas de formulario, foco visible y estados que no dependan solo del color.
- Diseño utilizable en una pantalla de 360 px de ancho y en escritorio.
- Mensajes de validación comprensibles y ausencia de trazas técnicas en las pantallas normales.
- Pruebas automáticas sobre reglas y permisos, más una prueba del ciclo completo.
- Configuración por entorno y ausencia de secretos o configuraciones de IDE en Git.
- No se fija un objetivo de carga o disponibilidad sin una medición y un entorno acordados.

## 8. Demostración de aceptación del producto

1. Un visitante abre el catálogo y no accede al contenido privado.
2. Un alumno se registra y solicita inscripción.
3. El profesor acepta y publica un material y una actividad abierta.
4. El alumno consulta el aula, la agenda y las instrucciones.
5. El alumno entrega texto y comprueba que quedó guardado.
6. Se utiliza una actividad de demostración ya cerrada con una entrega previa para corregir, o se reproduce el paso con un reloj controlado en pruebas.
7. El profesor registra nota y comentario.
8. El alumno consulta el resultado.
9. Otra cuenta intenta acceder a la entrega y recibe una denegación.

No se alterará el reloj del equipo ni se esperará días durante una demostración. Los datos ficticios incluirán actividades abiertas y cerradas coherentes.

## 9. Pendientes antes de empezar

| Decisión | Responsable | Momento |
| --- | --- | --- |
| Nombres y disponibilidad de las diez personas | Ambos equipos | Inicio |
| Fecha de entrega y alcance de la demostración | Ambos enlaces | Inicio |
| Aceptar o modificar RN08 y RN10 | Representantes de ambos perfiles | Antes de actividades y entregas |
| Archivos adjuntos obligatorios o ampliación | Ambos equipos | Antes de cerrar la semana 1 |
| Modelo Git y commits obligatorios del enunciado completo | Responsable de organización | Semana 1 |

Todo cambio posterior que afecte a ambos equipos se registra en un WI con impacto en alcance, datos, contratos, pruebas y fecha.
