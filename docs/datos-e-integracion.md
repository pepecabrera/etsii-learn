# ETSII Learn · Datos e integración

Versión 0.1 · 13 de noviembre de 2026 · Contrato inicial entre equipos.

Este documento define un modelo propuesto y contratos a implementar. No contiene DDL ejecutado ni una API ya disponible. Sus cambios deben coordinarse antes de modificar consumidores.

## 1. Propiedad y relaciones

| Entidad | Responsable | Relación principal |
| --- | --- | --- |
| usuarios | A1 | Cuenta con rol ALUMNO o PROFESOR. |
| asignaturas | A2 | Cada asignatura pertenece a un profesor. |
| inscripciones | A2 | Une un alumno con una asignatura y su estado. |
| materiales | A3 | Cada material pertenece a una asignatura. |
| actividades | A4 | Cada actividad pertenece a una asignatura. |
| entregas | B3 | Une alumno y actividad; una sola entrega por pareja. |
| evaluaciones | A5 | Cero o una evaluación por entrega. |

Una asignatura tiene muchos materiales, actividades e inscripciones. Una actividad puede tener muchas entregas. Una entrega puede existir sin evaluar. No existe una tabla de agenda: se consulta la información anterior.

## 2. Diccionario de datos propuesto

Todas las tablas usan InnoDB y utf8mb4. Las claves primarias son INT UNSIGNED autoincrementales. Las fechas persistidas usan DATETIME(6) con semántica UTC, documentada porque ese tipo no conserva zona horaria. Un campo es obligatorio salvo que se indique opcional.

### usuarios

| Campo | Tipo / regla |
| --- | --- |
| id | Clave primaria. |
| nombre | VARCHAR(100), no vacío. |
| email | VARCHAR(254), normalizado y único. |
| password_hash | VARCHAR(255), nunca contraseña en claro. |
| rol | VARCHAR(10), CHECK en ALUMNO o PROFESOR. |
| creado_en | DATETIME(6), UTC. |

La normalización del correo y la política de unicidad se comparten entre registro y provisión de docentes. No exigir un dominio institucional sin un requisito y un mecanismo de verificación.

### asignaturas

| Campo | Tipo / regla |
| --- | --- |
| id | Clave primaria. |
| codigo | VARCHAR(30), único, no vacío; identifica una instancia del aula. |
| nombre | VARCHAR(150), no vacío. |
| descripcion | TEXT, no vacía y pública. |
| curso_academico | VARCHAR(9), formato acordado como 2026-2027. |
| profesor_id | FK a usuarios; el servicio exige rol PROFESOR. |
| creado_en | DATETIME(6), UTC. |

Para repetir una materia en otro curso se crea otra instancia con otro código. No se incorpora un modelo separado de titulaciones, grupos y convocatorias al MVP.

### inscripciones

| Campo | Tipo / regla |
| --- | --- |
| id | Clave primaria. |
| asignatura_id | FK a asignaturas. |
| alumno_id | FK a usuarios; el servicio exige rol ALUMNO. |
| estado | VARCHAR(10), CHECK en PENDIENTE, ACEPTADA o RECHAZADA. |
| solicitada_en | DATETIME(6), UTC. |
| resuelta_en | DATETIME(6), opcional mientras esté pendiente. |

UNIQUE(asignatura_id, alumno_id). Coherencia: pendiente implica resuelta_en nula; aceptada o rechazada implica fecha de resolución. Solo el profesor responsable resuelve. No hay reapertura ni revocación en esta versión.

### materiales

| Campo | Tipo / regla |
| --- | --- |
| id | Clave primaria. |
| asignatura_id | FK a asignaturas. |
| titulo | VARCHAR(150), no vacío. |
| contenido | TEXT, texto plano obligatorio. |
| enlace | VARCHAR(2048), opcional; solo HTTP o HTTPS. |
| creado_en / actualizado_en | DATETIME(6), UTC. |

No es necesario almacenar profesor_id: se obtiene de la asignatura y evita duplicidades.

### actividades

| Campo | Tipo / regla |
| --- | --- |
| id | Clave primaria. |
| asignatura_id | FK a asignaturas. |
| titulo | VARCHAR(150), no vacío. |
| instrucciones | TEXT, texto plano obligatorio. |
| fecha_limite | DATETIME(6), UTC; futura al crear o editar. |
| creado_en / actualizado_en | DATETIME(6), UTC. |

La pertenencia a una asignatura no se cambia tras crear la actividad. Si existe alguna entrega, se rechaza editar o eliminar la actividad.

### entregas

| Campo | Tipo / regla |
| --- | --- |
| id | Clave primaria. |
| actividad_id | FK a actividades. |
| alumno_id | FK a usuarios. |
| contenido | TEXT, no vacío. |
| entregada_en | DATETIME(6), fecha de primera entrega en UTC. |
| actualizada_en | DATETIME(6), fecha de última edición en UTC. |

UNIQUE(actividad_id, alumno_id). El servicio comprueba rol, inscripción aceptada, autor y plazo. No se implementa borrado ni historial de versiones. Límite de producto inicial: 10 000 caracteres; con utf8mb4 este límite deja el contenido dentro de la capacidad de TEXT.

### evaluaciones

| Campo | Tipo / regla |
| --- | --- |
| id | Clave primaria. |
| entrega_id | FK a entregas y UNIQUE. |
| nota | DECIMAL(4,2), CHECK entre 0.00 y 10.00. |
| comentario | TEXT, no vacío. |
| evaluada_en | DATETIME(6), primera evaluación en UTC. |
| actualizada_en | DATETIME(6), última corrección en UTC. |

La identidad del profesor autorizado se deriva de la asignatura. Una modificación conserva evaluada_en y actualiza actualizada_en. No hay versiones históricas ni varios evaluadores.

### Integridad e índices

- FKs con borrado restringido para usuarios, asignaturas, inscripciones, actividades con entregas y entregas con evaluación. No usar cascadas para borrar trabajo académico.
- Índices sobre asignaturas.profesor_id, inscripciones(alumno_id, estado), actividades(asignatura_id, fecha_limite), materiales.asignatura_id y entregas.actividad_id.
- Las restricciones UNIQUE evitan duplicados incluso ante dos peticiones simultáneas.
- Las reglas entre tablas, como comprobar que el usuario es profesor, se verifican en servicios; un CHECK simple no puede resolverlas.
- No copiar nombres, notas o fechas en varias tablas para facilitar una pantalla.

## 3. Matriz de permisos

| Operación | Visitante | Alumno | Profesor |
| --- | --- | --- | --- |
| Ver catálogo y descripción | Sí | Sí | Sí |
| Crear asignatura | No | No | Sí, queda como responsable |
| Editar asignatura | No | No | Solo la propia |
| Solicitar inscripción | No | Para sí mismo | No |
| Resolver inscripción | No | No | Solo de su asignatura |
| Ver materiales y actividades | No | Si está aceptado | Si es responsable |
| Publicar o modificar materiales | No | No | Solo en su asignatura |
| Crear actividad | No | No | Solo en su asignatura |
| Editar o eliminar actividad | No | No | Solo propia y sin entregas |
| Entregar o editar trabajo | No | Solo propio, aceptado y antes del cierre | No |
| Ver una entrega | No | Solo propia | Si pertenece a su asignatura |
| Evaluar | No | No | Solo su asignatura y desde el cierre |
| Ver notas | No | Solo propias | Solo de su asignatura |
| Consultar agenda | No | Sus asignaturas aceptadas | Sus asignaturas |

La autorización se calcula a partir del recurso real. No basta con que el usuario sea profesor ni con comprobar el asignatura_id enviado en un formulario.

## 4. Estados y fechas

### Inscripción

| Estado inicial | Acción | Resultado |
| --- | --- | --- |
| No existe | Solicitar | PENDIENTE |
| PENDIENTE | Aceptar por profesor responsable | ACEPTADA |
| PENDIENTE | Rechazar por profesor responsable | RECHAZADA |
| ACEPTADA o RECHAZADA | Volver a resolver | Conflicto; no se modifica |

Una solicitud repetida no crea una segunda fila. La pantalla explica su estado actual.

### Estado derivado de una actividad para un alumno

Evaluar las condiciones en este orden:

| Condición | Estado visible |
| --- | --- |
| Tiene entrega con evaluación | Evaluada |
| Tiene entrega sin evaluación | Entregada · pendiente de evaluación |
| Sin entrega y ahora es anterior al cierre | Pendiente |
| Sin entrega y ahora es igual o posterior al cierre | Vencida sin entrega |

No hay un estado manual «completada» distinto de la entrega. No guardar el estado derivado en una columna que pueda quedar desactualizada.

### Frontera del cierre

Con T igual a fecha_limite:

- Entregar o editar: permitido solo si ahora < T.
- Evaluar: permitido si ahora >= T.
- No se admiten entregas tardías en el MVP.
- El navegador presenta la fecha, pero el servidor decide el instante válido.
- El reloj es sustituible únicamente en configuración o fixtures de pruebas, nunca mediante un parámetro público de petición.

## 5. Contratos internos de integración

Se proponen funciones de servicio dentro de la misma aplicación. No son endpoints de una API REST ni requieren comunicación HTTP entre equipos.

Convenciones: actor_id se obtiene de la sesión validada; los identificadores son enteros; los textos son Unicode; las fechas Python se representan como datetime con zona UTC. El repositorio adapta esas fechas al DATETIME UTC de MariaDB. Los listados vacíos devuelven una lista vacía.

| Contrato propuesto | Implementa | Resultado |
| --- | --- | --- |
| auth.current_user() | A1 | Usuario autenticado: id, nombre y rol; o ausencia de sesión. |
| asignaturas.listar_catalogo(filtros) | A2 | Campos públicos de asignaturas, sin datos privados. |
| asignaturas.solicitar_inscripcion(actor_id, asignatura_id) | A2 | Inscripción creada como pendiente; B1 lo consume. |
| asignaturas.resolver_inscripcion(actor_id, inscripcion_id, decision) | A2 | Inscripción aceptada o rechazada. |
| asignaturas.listar_aceptadas(actor_id) | A2 | Asignaturas privadas accesibles por ese alumno. |
| asignaturas.exigir_acceso(conn, actor_id, asignatura_id) | A2 | Autoriza acceso privado o lanza error; no confirma transacciones. |
| actividades.listar_para_alumno(actor_id, filtros) | A4 | Actividades de asignaturas aceptadas, con fechas e instrucciones. |
| actividades.obtener_para_entrega(conn, actor_id, actividad_id) | A4 | Actividad autorizada; permite bloqueo para escribir entrega. |
| entregas.guardar(actor_id, actividad_id, contenido, entrega_id=None) | B3 | Entrega creada o editada con sus fechas. |
| entregas.listar_para_docente(actor_id, actividad_id) | B3 | Entregas accesibles y datos mínimos de su autor. |
| entregas.obtener_propia(actor_id, actividad_id) | B3 | Entrega propia o ausencia de entrega. |
| evaluacion.guardar(actor_id, entrega_id, nota, comentario) | A5 | Evaluación creada o modificada. |
| evaluacion.listar_propias(actor_id, filtros) | A5 | Notas y comentarios propios para B5. |
| panel.listar_agenda(actor_id, filtros) | B4 | Actividades y estados derivados según el perfil. |

Los servicios de listado de asignaturas para profesor y consulta de materiales siguen las mismas reglas. Antes de programar, fijar nombres definitivos y pequeñas estructuras de retorno en un WI compartido.

Errores de dominio comunes propuestos: ValidacionError, PermisoError, NoEncontradoError y ConflictoError. Las rutas los convierten a las respuestas definidas en [Arquitectura](arquitectura.md). Los módulos no se intercambian mensajes de error SQL como contrato funcional.

### Forma mínima de los datos compartidos

| Objeto | Campos de retorno |
| --- | --- |
| Asignatura pública | id, codigo, nombre, descripcion, curso_academico, profesor_nombre |
| Inscripción | id, asignatura_id, alumno_id, estado, solicitada_en, resuelta_en |
| Actividad privada | id, asignatura_id, titulo, instrucciones, fecha_limite |
| Entrega autorizada | id, actividad_id, alumno_id, contenido, entregada_en, actualizada_en |
| Evaluación autorizada | entrega_id, nota, comentario, evaluada_en, actualizada_en |
| Fila de agenda | actividad_id, asignatura_id, asignatura_nombre, titulo, fecha_limite, estado |

No incluir password_hash en respuestas de presentación. Usar Decimal para notas en Python; convertir de forma explícita al presentar o serializar. Si se utiliza JSON para agenda, las fechas se expresan en ISO 8601 UTC con sufijo Z.

## 6. Rutas de integración orientativas

| Método | Ruta | Responsabilidad |
| --- | --- | --- |
| GET | /asignaturas | B1, consulta pública |
| GET / POST | /registro y /acceso | A1 |
| POST | /salir | A1 |
| GET | /mis-asignaturas | B2 |
| GET | /asignaturas/{id}/aula | B2, acceso privado |
| POST | /asignaturas/{id}/solicitudes | B1 invoca el servicio de A2 |
| GET | /docencia/asignaturas | A2 |
| POST | /docencia/inscripciones/{id}/resolver | A2 |
| GET / POST | /docencia/asignaturas/{id}/materiales/nuevo | A3 |
| GET / POST | /docencia/asignaturas/{id}/actividades/nueva | A4 |
| GET | /actividades/{id} | B2 con contrato de A4 |
| GET / POST | /actividades/{id}/entrega | B3 |
| GET | /docencia/actividades/{id}/entregas | A5 con contrato de B3 |
| GET / POST | /docencia/entregas/{id}/evaluacion | A5 |
| GET | /agenda | B4 |
| GET | /resultados | B5 |

Las rutas de editar y eliminar se completarán sin cambiar la propiedad de módulos. Dos equipos no deben registrar la misma ruta con controladores distintos.

## 7. Transacciones y concurrencia

Para escribir una entrega:

1. Abrir la transacción del servicio y bloquear la actividad.
2. Comprobar usuario, inscripción aceptada y plazo con la hora actual del servidor.
3. Crear o bloquear y editar la entrega propia.
4. Aplicar la restricción única y confirmar; ante error, deshacer.

Para editar o eliminar una actividad se bloquea la misma fila antes de comprobar la ausencia de entregas. Así se evita aceptar una edición mientras otra petición crea la primera entrega.

Para evaluar: bloquear primero la actividad y después la entrega, comprobar profesor y cierre, y crear o actualizar la evaluación en la misma transacción. Mantener ese orden cuando una operación necesite varios de estos recursos.

La resolución de inscripción bloquea su fila y exige que siga pendiente. No hay confirmaciones parciales ni commits internos en repositorios.

## 8. Datos ficticios de demostración

| Datos | Propósito |
| --- | --- |
| Dos profesores | Probar propiedad de asignaturas y rechazo entre docentes. |
| Tres alumnos | Probar aislamiento de entregas y alumno no inscrito. |
| Dos asignaturas | Comprobar filtros y separación del contenido. |
| Inscripciones aceptadas, pendientes y rechazadas | Probar todos los accesos. |
| Materiales de texto y enlaces | Ver contenido privado sin adjuntos. |
| Actividad abierta | Demostrar creación y edición de entrega. |
| Actividad cerrada con entrega previa | Demostrar evaluación sin esperar al cierre. |
| Entrega evaluada y otra sin evaluar | Comprobar resumen y resultados. |

Generar fechas coherentes respecto al día de creación del conjunto. Una entrega de una actividad cerrada debe tener una fecha anterior al cierre. Las cuentas son ficticias y sus contraseñas se proporcionan fuera del control de versiones.

## 9. Primera integración y cambios

La primera prueba compartida crea una actividad con A4 y la consulta desde B2 y B4 con un alumno aceptado. La segunda registra una entrega de B3 y la consulta desde A5. La tercera devuelve una evaluación y la presenta en B5.

No utilizar copias de tablas ni datos simulados para dar por terminada una integración. Los dobles de prueba son válidos en pruebas unitarias; las pruebas compartidas utilizan los servicios y MariaDB reales.

Cuando cambie un contrato: registrar el WI, identificar consumidores, actualizar este documento y aplicar implementación y pruebas de forma coordinada. No basta con avisar por chat.
