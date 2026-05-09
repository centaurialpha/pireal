# Operadores

Pireal soporta los operadores centrales del Álgebra Relacional. Todas las consultas siguen esta sintaxis:

```
nombre_resultado := expresión;
```

---

## Operadores unarios

Toman una sola relación como entrada.

### Selección - `select`

Filtra las filas que satisfacen una condición. Devuelve una relación con las mismas columnas pero solo las filas que cumplen el criterio.

```
resultado := select condición (relación);
```

**Ejemplo:**

```
adultos := select edad >= 18 (alumno);
```

**Operadores de comparación:**

| Operador | Significado   |
|----------|---------------|
| `=`      | igual         |
| `<>`     | distinto      |
| `<`      | menor que     |
| `<=`     | menor o igual |
| `>`      | mayor que     |
| `>=`     | mayor o igual |

**Operadores lógicos** `and`/`or` para combinar condiciones:

```
resultado := select edad >= 18 and edad <= 30 (alumno);
```

**Comparar con strings y fechas:**

```
resultado := select nombre = 'Juan' (alumno);
resultado := select fecha_inicio > '01/03/2017' (curso);
```

---

### Proyección - `project`

Selecciona columnas específicas de una relación.

```
resultado := project col1, col2 (relación);
```

**Ejemplo:**

```
nombres := project nombre (alumno);
```

!!! warning "Eliminación de duplicados"
    La proyección elimina automáticamente las filas duplicadas, ya que las relaciones son conjuntos.

---

## Operadores binarios

Toman dos relaciones como entrada.

### Join Natural - `njoin`

Une dos relaciones por las columnas que comparten el mismo nombre. Solo incluye las filas donde los valores de las columnas compartidas coinciden en ambas relaciones.

```
resultado := izquierda njoin derecha;
```

**Ejemplo:**

```
resultado := alumno njoin inscripto;
```

---

### Outer Joins

Como el join natural, pero conservan las filas sin coincidencia, rellenando los valores faltantes con `null`.

| Sintaxis         | Conserva filas sin match de... |
|------------------|-------------------------------|
| `izq louter der` | relación izquierda            |
| `izq router der` | relación derecha              |
| `izq fouter der` | ambas relaciones              |

**Ejemplo:**

```
% Todos los alumnos, incluso los que no están inscriptos en ningún curso
resultado := alumno louter inscripto;
```

---

### Unión - `union`

Devuelve todas las filas de ambas relaciones. Ambas deben tener exactamente las mismas columnas — mismos nombres y mismo orden. Los duplicados se eliminan.

```
resultado := r1 union r2;
```

---

### Intersección - `intersect`

Devuelve solo las filas que aparecen en ambas relaciones.

```
resultado := r1 intersect r2;
```

---

### Diferencia - `difference`

Devuelve las filas que están en la primera relación pero no en la segunda.

```
resultado := r1 difference r2;
```

---

### Producto cartesiano - `product`

Devuelve todas las combinaciones posibles de filas de ambas relaciones.

```
resultado := r1 product r2;
```

!!! warning "Resultados grandes"
    Si `r1` tiene 100 filas y `r2` tiene 50, el producto tiene 5.000 filas. Usarlo con cuidado.

---

## Anidamiento de expresiones

Los operadores se pueden anidar libremente:

```
q1 := alumno njoin (inscripto njoin curso);
q2 := project nombre, nombre_curso (q1);
q3 := select nombre_curso = 'Python' (q2);
```

---

## Comentarios

Las líneas que empiezan con `%` son comentarios:

```
% Selecciona todos los alumnos adultos
adultos := select edad >= 18 (alumno);
```

---

## ~~¿Y la división?~~

~~El operador de división no está implementado directamente en Pireal, y es intencional. La división puede expresarse combinando los operadores que ya tenés: producto cartesiano, diferencia y proyección.~~

~~Deducir cómo hacerlo es un ejercicio excelente para entender el Álgebra Relacional en profundidad. Si llegás a la solución, significa que realmente entendés cómo funciona.~~

!!! success "Actualización: la división ya está implementada"
    El ejercicio era tan bueno que terminé implementándolo. Ver más abajo.

### División - `divide`

Devuelve todas las tuplas de la relación **izquierda** (proyectadas sobre las columnas que no están en la derecha) tales que se combinan con **cada** tupla de la relación derecha y esa combinación existe en la relación izquierda.

En términos prácticos: encontrá cada valor en R que esté "emparejado con todos" los valores en S.

```
resultado := dividendo divide divisor;
```

**Precondiciones:**

- Las columnas del divisor deben ser un subconjunto de las columnas del dividendo.
- El dividendo debe tener al menos una columna que no esté en el divisor.

**Ejemplo:**

Encontrar todos los alumnos inscriptos en todos los cursos disponibles:

```
inscripciones  := project id_alumno, cod_curso (inscripto);
todos_cursos   := project cod_curso (curso);
en_todos       := inscripciones divide todos_cursos;
```

**Símbolo unicode:** se puede usar `÷` en lugar de `divide`:

```
en_todos := inscripciones ÷ todos_cursos;
```

!!! note "Columnas del resultado"
    El resultado contiene solo las columnas del dividendo que **no** están presentes en el divisor. En el ejemplo, el resultado tiene únicamente `id_alumno`.
