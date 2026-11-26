# Diseño

Bootstrap 5 ya resuelve los componentes (botones, formularios, tarjetas, tablas, navegación). Este documento solo fija las decisiones comunes para que las once pantallas parezcan una sola aplicación. Si algo no aparece aquí, se usa Bootstrap por defecto.

## Identidad

- **Nombre y logo:** texto «ETSII Learn» con el icono `bi-mortarboard` de Bootstrap Icons. Es un logo propio del proyecto.
- No se usan escudos ni logotipos oficiales de la Universidad o de la escuela.

## Colores

Se mantiene la paleta de Bootstrap y solo se cambia el color principal. Se define una vez en `static/css/custom.css`, sobrescribiendo las variables CSS de Bootstrap:

```css
:root {
  --bs-primary: #1D4ED8;
  --bs-primary-rgb: 29, 78, 216;
  --bs-link-color: #1D4ED8;
}
```

Si el botón principal no cambia de color con esta sobrescritura, se ajusta también `.btn-primary` en el mismo archivo. Se comprueba una vez que el texto blanco sobre el color principal tenga buen contraste.

| Uso | Clase Bootstrap |
| --- | --- |
| Acción principal y enlaces | `primary` |
| Éxito, aceptado, evaluado | `success` |
| Pendiente o atención | `warning` |
| Error, rechazo, borrar | `danger` |
| Neutro, inactivo | `secondary` |
| Información secundaria | `text-secondary` |

## Botones

- **Una sola acción principal por pantalla o bloque:** `btn btn-primary` («Entregar trabajo», «Guardar actividad»).
- **Acciones alternativas:** `btn btn-outline-secondary` («Volver», «Cancelar»).
- **Borrar:** `btn btn-danger`, con texto explícito («Eliminar material») y confirmación antes de ejecutar.
- Los enlaces sirven para navegar y los botones para ejecutar acciones.

## Estados

Los estados siempre se muestran con una insignia (`badge`) que lleva texto. El color nunca es lo único que los distingue.

| Estado | Insignia |
| --- | --- |
| Pendiente | `text-bg-warning` |
| Vencida sin entrega | `text-bg-danger` |
| Entregada · pendiente de evaluación | `text-bg-primary` |
| Evaluada | `text-bg-success` |
| Inscripción aceptada | `text-bg-success` |
| Inscripción de baja | `text-bg-secondary` |
| Inscripción bloqueada | `text-bg-danger` |

## Plantilla y componentes compartidos

Todas las páginas heredan de `templates/base.html`, que incluye la barra de navegación, los mensajes `flash` y el bloque de contenido. Se reutilizan siempre los mismos componentes:

- Tarjeta de asignatura (código, nombre, profesor principal, estado de la inscripción).
- Fila de actividad (título, asignatura, cierre, insignia de estado).
- Mensaje de confirmación o error (`alert`).
- Estado vacío: un texto que explica que no hay datos y, si procede, un botón con la siguiente acción.

Los cambios en `base.html` o en estos componentes se avisan al resto del equipo mediante un WI.

## Navegación

| Contexto | Opciones |
| --- | --- |
| Sin sesión | Acceder, Registrarse |
| Alumno | Inicio, Mis asignaturas, Agenda, Resultados, Solicitudes, Cerrar sesión |
| Profesor | Inicio, Mis asignaturas, Agenda, Cerrar sesión |

- El nombre y el rol del usuario aparecen en la cabecera.
- No se muestran botones de funciones que todavía no existan.
- Dentro de un aula: el alumno ve Materiales y Actividades. El profesor, Materiales, Actividades, Inscripciones y Profesores.

## Textos y fechas

- Tono directo: «Guardar actividad», «Entrar con el código», «Ver evaluación».
- **Entrega** es el trabajo del alumno. **Actividad** es el encargo del profesor.
- Fechas con el formato «18 nov 2026, 23:59», en hora de Madrid.
- Los errores explican cómo arreglarlos («La nota debe estar entre 0 y 10»). No se muestran SQL, trazas ni nombres de tablas.

## Formularios

- Cada campo lleva su etiqueta (`<label>`); el placeholder no la sustituye.
- Si la validación falla, el formulario conserva lo escrito y muestra el error junto al campo.
- Las tablas largas usan `table-responsive` para que funcionen en móvil.

## Comprobación antes de dar una pantalla por terminada

- [ ] Hereda de `base.html` y usa los componentes comunes.
- [ ] Tiene estado vacío y mensajes de error cuando corresponde.
- [ ] Se puede usar con teclado y a 360 px de ancho.
- [ ] Los estados llevan texto, no solo color.
- [ ] Las fechas y los nombres de los estados coinciden con los del resto de la aplicación.