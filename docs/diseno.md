# ETSII Learn · Diseño e interfaz

Versión 0.1 · 13 de noviembre de 2026 · Propuesta visual inicial.

## 1. Dirección

Una interfaz académica clara, tranquila y centrada en tareas. La asignatura es la unidad de navegación. El alumno debe localizar lo que tiene pendiente y el profesor debe encontrar las entregas que necesita revisar.

La identidad visual propuesta es propia del proyecto; no se presenta como manual de marca oficial de la Universidad o de la escuela. No se incorporarán escudos o logotipos oficiales sin confirmar su uso.

## 2. Paleta propuesta

| Token CSS | Color | Uso |
| --- | --- | --- |
| --color-primary | #1D4ED8 | Botón principal, enlaces y selección. |
| --color-primary-hover | #1E40AF | Interacción sobre la acción principal. |
| --color-accent | #0F766E | Éxito y estado evaluado. |
| --color-text | #0F172A | Texto principal. |
| --color-muted | #475569 | Información secundaria. |
| --color-background | #F8FAFC | Fondo general. |
| --color-surface | #FFFFFF | Tarjetas, formularios y tablas. |
| --color-border | #CBD5E1 | Separación decorativa de bloques. |
| --color-control-border | #64748B | Contorno visible de campos y controles. |
| --color-warning | #92400E | Pendiente o atención. |
| --color-warning-bg | #FEF3C7 | Fondo de avisos. |
| --color-danger | #B91C1C | Error, rechazo o acción destructiva. |
| --color-danger-bg | #FEE2E2 | Fondo de errores. |
| --color-success-bg | #CCFBF1 | Fondo de confirmación. |

Texto blanco sobre primary, primary-hover, accent y danger. Texto text o muted sobre superficies claras. Warning sobre warning-bg, danger sobre danger-bg y accent sobre success-bg. No usar border como único límite funcional de un campo: para eso existe control-border.

Verificar contraste de cualquier combinación nueva. Objetivo: al menos 4.5:1 en texto normal y 3:1 en texto grande y elementos funcionales pertinentes. El color nunca sustituye una etiqueta de estado.

## 3. Tipografía y medidas

- Fuente del sistema: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif.
- Texto base: 16 px y altura de línea 1.5.
- Texto secundario: 14 px como referencia; no reducir instrucciones importantes para hacerlas caber.
- Título de página: 28–32 px; título de sección: 22–24 px; título de tarjeta: 18–20 px.
- Escala de espacios: 4, 8, 12, 16, 24, 32 y 48 px.
- Radio de campos y botones: 8 px; tarjetas: 12 px.
- Ancho de contenido: hasta 1200 px; formularios de lectura o escritura: aproximadamente 720 px.
- Controles principales: altura objetivo de 44 px o más.

La primera implementación de tokens puede partir del siguiente fragmento. Es una especificación para el futuro tokens.css, no un fichero CSS adicional incluido.

~~~css
:root {
  --color-primary: #1D4ED8;
  --color-primary-hover: #1E40AF;
  --color-accent: #0F766E;
  --color-text: #0F172A;
  --color-muted: #475569;
  --color-background: #F8FAFC;
  --color-surface: #FFFFFF;
  --color-border: #CBD5E1;
  --color-control-border: #64748B;
  --color-warning: #92400E;
  --color-warning-bg: #FEF3C7;
  --color-danger: #B91C1C;
  --color-danger-bg: #FEE2E2;
  --color-success-bg: #CCFBF1;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --radius-control: 0.5rem;
  --radius-card: 0.75rem;
}
~~~

## 4. Navegación

| Contexto | Opciones |
| --- | --- |
| Sin sesión | ETSII Learn, Catálogo, Acceder y Registrarse. |
| Alumno | Inicio, Mis asignaturas, Agenda, Resultados, Solicitudes y Cerrar sesión. |
| Profesor | Inicio, Mis asignaturas, Agenda y Cerrar sesión. La corrección se encuentra dentro de cada actividad. |

El nombre y el rol aparecen en la cabecera. No hay selector público para convertirse en profesor. No ofrecer botones de funcionalidades futuras que no estén implementadas.

Dentro del aula:

- Alumno: Materiales y Actividades; la nota se consulta en cada actividad y en Resultados.
- Profesor: Materiales, Actividades e Inscripciones.

Usar una única plantilla base y componentes compartidos. En móvil, la navegación puede abrirse con un botón etiquetado; no depender de un icono sin nombre accesible.

## 5. Componentes comunes

| Componente | Comportamiento |
| --- | --- |
| Botón principal | Una acción destacada por bloque, como «Entregar trabajo». |
| Botón secundario | Acción alternativa, como volver o editar. |
| Botón destructivo | Texto explícito y confirmación cuando elimina un material o actividad sin entregas. |
| Campo de formulario | Etiqueta, ayuda si procede y error asociado; no usar placeholder como etiqueta. |
| Tarjeta de asignatura | Código, nombre, profesor y acceso o estado de solicitud. |
| Fila de actividad | Título, asignatura, cierre y estado textual. |
| Insignia de estado | Texto más color; nunca una marca de color aislada. |
| Mensaje de confirmación | Explica qué se guardó; no desaparece antes de poder leerse. |
| Estado vacío | Explica que no hay datos y ofrece una acción cuando corresponde. |
| Tabla | Cabeceras claras y adaptación a móvil sin perder acciones. |
| Migas de navegación | Asignatura → actividad → entrega o evaluación. |

Los formularios mantienen el contenido si falla la validación. Durante el envío puede deshabilitarse temporalmente el botón, pero la protección contra duplicados también existe en el servidor.

## 6. Bocetos funcionales de las pantallas principales

Estos bocetos describen jerarquía y contenido; no son capturas de una aplicación ya construida.

### P01 · Catálogo público

| Orden | Contenido |
| --- | --- |
| Cabecera | Marca del proyecto, acceso y registro. |
| Encabezado | «Explora las asignaturas» y breve explicación. |
| Filtros | Texto por nombre o código; curso académico si aporta valor. |
| Resultado | Tarjetas con nombre, código, curso, profesor y descripción breve. |
| Detalle | Información pública y acción «Solicitar inscripción» tras acceder como alumno. |

No mostrar alumnos inscritos, materiales, fechas de actividades ni notas.

### P02 · Aula de asignatura

| Orden | Alumno | Profesor |
| --- | --- | --- |
| Encabezado | Nombre, código y profesor | Nombre, código y acceso a edición |
| Navegación local | Materiales y Actividades | Materiales, Actividades e Inscripciones |
| Contenido | Listado privado consultable | Listado con acciones de gestión |
| Actividad | Título, cierre y estado propio | Título, cierre y número de entregas |

El alumno pendiente o rechazado ve su solicitud, no una versión parcial del aula.

### P03 · Detalle de actividad

1. Ruta de vuelta a la asignatura.
2. Título, asignatura, fecha límite y estado.
3. Instrucciones completas.
4. Bloque «Tu entrega» con texto guardado y fecha de modificación.
5. Acción para entregar o editar si el plazo sigue abierto.
6. Bloque de evaluación con nota y comentario cuando exista.

Si el plazo ha terminado sin entrega, explicar «El plazo ha terminado y no consta una entrega». No presentar un botón aparentemente activo que vaya a fallar.

### P04 · Formulario de entrega

- Encabezado con actividad y cierre.
- Área de texto grande con etiqueta «Contenido de tu entrega».
- Indicación del límite de caracteres y validación en servidor.
- Acción «Entregar trabajo» para el primer envío o «Guardar cambios» para editar.
- Confirmación con fecha y hora tras guardar.

Sin guardado automático en el MVP. No prometer recuperación de un borrador que no se ha enviado.

### P05 · Corrección del profesor

En escritorio: trabajo del alumno y formulario de evaluación en dos columnas cuando haya espacio. En móvil: contenido primero, formulario después.

- Alumno, actividad y fecha de entrega.
- Texto entregado.
- Nota numérica de 0 a 10 con hasta dos decimales.
- Comentario obligatorio.
- Acción «Guardar evaluación» o «Actualizar evaluación».
- Antes del cierre: lectura disponible y explicación de por qué todavía no se evalúa.

### P06 · Agenda

Vista inicial en listado ordenado por fecha, agrupable por día o semana.

| Perfil | Información |
| --- | --- |
| Alumno | Asignatura, actividad, cierre y pendiente / vencida sin entrega / entregada / evaluada. |
| Profesor | Asignatura, actividad, cierre, abierta o cerrada, número de entregas y número de evaluaciones. |

Filtros: asignatura y rango de fechas. No utilizar estados personales de alumno para describir la agenda del profesor.

### P07 · Resultados

Listado por asignatura y actividad con nota, comentario y fecha de evaluación. Las actividades entregadas sin corregir indican «Pendiente de evaluación». El resumen muestra cantidades por estado; no una media final que no se ha definido.

## 7. Lenguaje y fechas

- Tono directo y académico: «Guardar actividad», «Solicitar inscripción», «Ver evaluación».
- «Entrega» significa el trabajo guardado por el alumno; «actividad» significa el encargo del profesor.
- Mostrar fechas como «18 nov 2026, 23:59» e indicar que se usa la hora de Madrid.
- Si se muestra «vence mañana», mantener también la fecha exacta.
- Los errores explican la solución: «La nota debe estar entre 0 y 10».
- No mostrar SQL, nombres de tablas, trazas o excepciones al usuario.

## 8. Accesibilidad y adaptación

- Un título principal por pantalla y jerarquía coherente de encabezados.
- Enlaces para navegar y botones para realizar acciones.
- Foco visible con contorno primary y separación respecto al componente.
- Orden de tabulación natural y acceso por teclado a todos los controles.
- Etiquetas y errores conectados al campo correspondiente.
- No comunicar aceptación, rechazo o vencimiento únicamente con color.
- A 360 px, los formularios y acciones deben seguir siendo utilizables.
- Comprobar zoom al 200 %, nombres largos y textos de error.
- Usar confirmaciones y elementos HTML nativos cuando reduzcan problemas de interacción.

## 9. Coordinación visual

A3 y B2 preparan la primera plantilla base, tokens y componentes junto con una pantalla de cada perfil. El resto reutiliza esa base. Cambios en navegación o componentes compartidos se registran y comunican.

Checklist de revisión de una pantalla:

- [ ] Usa la plantilla y los componentes comunes.
- [ ] Tiene estados vacío, válido y de error cuando correspondan.
- [ ] Su contenido coincide con los permisos reales.
- [ ] Se utiliza con teclado y desde móvil.
- [ ] Muestra fechas y estados coherentes con el resto del producto.
- [ ] No incorpora funciones fuera de alcance ni detalles internos de implementación.
