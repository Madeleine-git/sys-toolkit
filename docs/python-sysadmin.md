# Por qué un administrador de sistemas necesita Python además de Bash

## El papel de Bash: rápido y directo

Bash es el lenguaje nativo del terminal. Para tareas directas
como renombrar ficheros, lanzar servicios o encadenar comandos,
es insustituible. Cuando escribes `ls | grep ".log" | sort`
estás orquestando el sistema con su propio idioma.

## Dónde Bash se queda corto

El problema aparece cuando la complejidad aumenta:

- **Análisis de datos estructurados.** Procesar un CSV con
  10.000 filas en Bash implica awk, sed y mucha paciencia.
  En Python, pandas lo resuelve en 5 líneas.

- **Llamadas a APIs REST.** Las herramientas modernas de
  seguridad exponen APIs HTTP. Bash puede hacer curl, pero
  manejar JSON y gestionar errores se vuelve frágil.

- **Legibilidad y mantenimiento.** Un script Bash de 200
  líneas es difícil de mantener. Python obliga a estructurar
  el código de forma más clara.

- **Testing.** No existe un ecosistema de tests robusto para
  Bash. Python tiene pytest, con el que verificas que tu
  auditor SSH funciona antes de desplegarlo.

- **Programación orientada a objetos.** Modelar entidades
  como Router, Server o EventoSSH como clases hace el código
  reutilizable y testeable.

## La regla práctica

| Situación                              | Herramienta        |
|----------------------------------------|--------------------|
| Automatizar comandos del sistema       | Bash               |
| Procesar texto simple (grep, sed)      | Bash               |
| Parsear ficheros de log complejos      | Python (re)        |
| Manipular tablas CSV / Excel           | Python (pandas)    |
| Consumir APIs REST                     | Python (requests)  |
| Generar informes automatizados         | Python (openpyxl)  |
| Proyectos con múltiples módulos        | Python             |

## Conclusión

No se trata de elegir uno u otro. Bash para interacción
directa con el sistema, Python cuando la complejidad lo
justifica. La combinación de ambos es la marca de un
administrador de sistemas moderno.