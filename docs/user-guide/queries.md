# Consultas

Los archivos de consultas (`.pqf`) contienen las expresiones de Álgebra Relacional a evaluar contra una base de datos abierta. Son archivos de texto plano que podés guardar, compartir y reutilizar.

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

Con una base de datos abierta, presioná **F5** o ir a **Consulta -> Ejecutar**.

!!! warning "Se necesita una base de datos abierta"
    Las consultas necesitan una base de datos para ejecutarse. Abrí o creá una antes de ejecutar.

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

Si una consulta tiene un error, Pireal muestra un mensaje descriptivo. Algunos ejemplos comunes:

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

## Funciones extra

### Árbol de sintaxis (AST)

Pireal puede mostrarte el árbol que construye internamente al parsear tu consulta. Es una forma concreta de ver cómo un intérprete "entiende" tu código, muy útil si estás cursando Compiladores o simplemente tenés curiosidad.

Activalo desde **Consulta -> Ver AST**.

### Generador de SQL

Cada consulta de Álgebra Relacional tiene un equivalente en SQL. Pireal puede generarlo automáticamente para que puedas comparar ambos lenguajes y entender cómo se relacionan.

Activalo desde **Consulta -> Generar SQL**.

---

## Modo terminal

Si preferís trabajar desde la línea de comandos, Pireal tiene un modo REPL que corre sin interfaz gráfica:

```bash
pireal --terminal mi_base.pdb
```

Si omitís el archivo, Pireal te lo pide al arrancar.

Una vez dentro, escribís consultas igual que en la interfaz, terminando con `;` para ejecutar:

```
pireal> q := select edad >= 18 (estudiantes);
```

Los resultados se muestran directamente en la terminal. Las consultas que ocupan más de una línea también funcionan, Pireal espera hasta que encontrás el `;`:

```
pireal> q := project nombre (
     …      select edad >= 18 (estudiantes)
     …  );
```

**Comandos disponibles:**

| Comando      | Acción                              |
|--------------|-------------------------------------|
| `\h`         | Mostrar ayuda                       |
| `\r`         | Listar las relaciones cargadas      |
| `\r nombre`  | Ver el contenido de una relación    |
| `exit` / `quit` / `:q` | Salir                  |

---

## Tips

- Dividí las consultas complejas en pasos con nombres intermedios, es más fácil de entender y depurar.
- Usá comentarios para explicar qué hace cada paso.
- Podés volver a ejecutar las consultas después de modificar la base de datos sin reiniciar Pireal.
