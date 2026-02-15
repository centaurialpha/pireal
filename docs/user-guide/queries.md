# Consultas

Los archivos de consultas (`.pqf`) contienen las expresiones de Álgebra Relacional a evaluar contra una base de datos. Son archivos de texto plano que podés guardar, compartir y reutilizar.

---

## Escribir consultas

Cada consulta es una asignación:

```
nombre_resultado := expresión;
```

El `:=` asigna el resultado de la expresión a un nombre. Ese nombre aparece en la barra lateral y puede usarse en expresiones posteriores.

Múltiples consultas en el mismo archivo se ejecutan en orden, de arriba hacia abajo:

```
q1 := select edad >= 18 (estudiantes);
q2 := project nombre (q1);
```

---

## Ejecutar consultas

Con una base de datos abierta, presioná **F5** o ir a **Consulta → Ejecutar**.

!!! warning "Se necesita una base de datos abierta"
    Las consultas necesitan una base de datos para ejecutarse. Abrí o creá una base de datos antes de ejecutar consultas.

---

## Comentarios

Usá `%` para agregar comentarios:

```
% Seleccionar estudiantes mayores de 18
adultos := select edad >= 18 (estudiantes);

q := project nombre (adultos);  % solo nombres
```

---

## Mensajes de error

Si una consulta tiene un error, Pireal muestra un mensaje descriptivo. Errores comunes:

**Relación no definida:**

```
q := select edad = 25 (typo);
% Error: La relación 'typo' no está definida
```

**Atributo no definido:**

```
q := project inexistente (estudiantes);
% Error: El atributo 'inexistente' no está definido en la relación 'estudiantes'
```

**Nombre de resultado duplicado:**

```
q := select edad = 25 (estudiantes);
q := project nombre (estudiantes);
% Error: Ya existe un resultado llamado 'q'
```

---

## Ejemplo de archivo de consultas

```
% === Análisis de estudiantes y cursos ===

% Todos los estudiantes inscriptos en algún curso
inscriptos := estudiantes njoin inscripciones;

% Cursos con valor menor a 3000
accesibles := select valor < 3000 (cursos);

% Estudiantes inscriptos en cursos accesibles
q1 := inscriptos njoin accesibles;
q2 := project nombre, nombre_curso (q1);

% Cursos que comienzan después de marzo (referencia)
cursos_tardios := select fecha_inicio > '01/03/2017' (cursos);
```

---

## Tips

- Dividí las consultas complejas en pasos con nombres intermedios — es más fácil de depurar y entender.
- Usá comentarios para explicar qué hace cada paso.
- Podés volver a ejecutar las consultas después de modificar la base de datos o el archivo de consultas sin reiniciar Pireal.

---

## Más funciones

### Árbol de sintaxis (AST)

<!-- SCREENSHOT: vista del AST generado para una consulta -->

Pireal puede mostrarte el árbol de sintaxis abstracta que construye internamente al parsear tu consulta. Es una forma concreta de ver cómo un intérprete "entiende" tu código — muy útil si estás cursando Compiladores o simplemente tenés curiosidad.

### Generador de SQL

<!-- SCREENSHOT: panel con el SQL generado -->

Cada consulta de Álgebra Relacional tiene un equivalente en SQL. Pireal puede generarlo automáticamente, lo que permite comparar ambos lenguajes y entender la relación entre ellos.

### Escribir la base de datos como código

<!-- SCREENSHOT: editor con sintaxis .pdb -->

En lugar de usar el formulario de creación de relaciones, podés escribir tu base de datos directamente en texto. Es más rápido, más fácil de compartir y se lleva bien con git.
