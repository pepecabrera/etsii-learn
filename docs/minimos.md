# Mínimos para superar el proyecto

El proyecto es un proyecto que tiene muchos elementos que se pueden y deben evaluar por lo que su evaluación depende mucho del tipo de proyecto, de la envergadura, de su complejidad, etcétera. De todos modos, entre los tutores, hemos acordado un conjunto de criterios mínimos para poder superar el proyecto. Superar el proyecto para nosotros significa tener una nota de al menos 5.

## Sobre el proyecto en sí:
- Debe presentar un proyecto funcional que realice un ciclo funcional completo y que pueda usarse (a pesar de que tenga algunos elementos de mejora)
- No pueden presentarse como proyectos subsistemas aislados en los que se evoluciona una parte y se deja atrás el resto. No se aceptarán proyectos que hagan funcionalidades de manera aislada sin una integración real.
- Debe haber al menos un "WI" por miembro del equipo.

## Sobre la gestión de cambio e incidencias sobre work items:
- Debe tener un proceso de gestión de Work Items (WIs) en el que los WIs pasen por una serie de estados, sean de una serie de tipos, tengan asignados unos roles en su gestión y una prioridad.
- Debe tener una plantilla para los WIs y esa plantilla debe ser usada de manera homogenea al menos en los WIs más cercanas a la entrega.

## Sobre la gestión del código:
- Debe crear un único repositorio entregable para el proyecto. Puede usar más repositorios si lo cree necesario, pero debe tener un solo repositorio para la entrega.
- No podrá hacer pull requests (PRs) dentro de un mismo equipo. Solo se admitrán PRs para proponer cambios que impliquen a más de un equipo y deben estar justificados.
- Los commits deben hacerse con el mismo nombre de usuario para cada componente del equipo. Si hay N componentes, debe haber N nombres de usuarios. Por cada nombre de usuario adicional se penalizará.
- No hará commits desde el propio portal de github. Siempre debe hacer commit en el repositorio local y luego sincronizarlo con el remoto.
- Debe tener un repositorio de código en el que se haya guardado toda la historia del proyecto.
- Debe tener al menos los commits que se indican en el enunciado y una participación homogénea de commits por parte de todos los componentes del equipo.
- Debe tener un patrón a la hora de hacer commits y este debe haber sido usado de manera homogénea al menos en las etapas finales del proyecto.
- No debe tener en control de versiones los ficheros de configuración de los IDEs ni otro tipo de información que no corresponde como credenciales de acceso a APIs, bases de datos, etcétera.
- Debe usar el modelo de uso del repositorio que se le enseña en clases de teoría/prácticas y solo se permitirán variaciones si están suficientemente justificadas.
- Sobre la gestión de la construcción e integración continua:
- Debe tener un servidor de integración continua funcionando y conectado con el repositorio de código.
- Debe tener al menos un script de construcción y que dicho script sea personalizado con respecto a su proyecto (se verá mal que el script sea el mismo que el del proyecto original).
- Debe tener integrada alguna prueba.


## Sobre el despliegue:
- Debe tener desplegado el sistema de manera local (con run server o similar).
- Debe tener desplegado el sistema con contenedores (docker)