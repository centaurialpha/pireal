# Operadores

Pireal soporta los operadores centrales del Álgebra Relacional. Todas las consultas siguen esta sintaxis:

```
nombre_resultado := expresión;
```

---

## Operadores unarios

Toman una sola relación como entrada.

### Selección — `select`

Filtra las filas que satisfacen una condición. Devuelve una relación con las mismas columnas pero solo las filas que cumplen el criterio.

```
resultado := select condición (relación);
```

**Ejemplo:**

```
adultos := select edad >= 18 (estudiantes);
```

**Operadores de comparación:**

| Operador | Significado    |
|----------|----------------|
| `=`      | igual          |
| `<>`     | distinto       |
| `<`      | menor que      |
| `<=`     | menor o igual  |
| `>`      | mayor que      |
| `>=`     | mayor o igual  |

**Operadores lógicos** `and` / `or` para combinar condiciones:

```
resultado := select edad >= 18 and edad <= 30 (estudiantes);
```

**Comparar con strings y fechas:**

```
resultado := select nombre = 'Gabriel' (estudiantes);
resultado := select fecha_inicio > '01/03/2017' (cursos);
```

---

### Proyección — `project`

Selecciona columnas específicas de una relación.

```
resultado := project col1, col2 (relación);
```

**Ejemplo:**

```
nombres := project nombre (estudiantes);
```

!!! warning "Eliminación de duplicados"
    La proyección elimina automáticamente las filas duplicadas, ya que las relaciones son conjuntos.

---

## Operadores binarios

Toman dos relaciones como entrada.

### Join Natural — `njoin`

Une dos relaciones por las columnas que comparten el mismo nombre.

```
resultado := izquierda njoin derecha;
```

**Ejemplo:**

```
inscriptos := estudiantes njoin inscripciones;
```

---

### Outer Joins

Como el join natural, pero conservan las filas sin coincidencia, rellenando los valores faltantes con `null`.

| Sintaxis                  | Conserva filas sin match de... |
|---------------------------|-------------------------------|
| `izq louter der`          | relación izquierda             |
| `izq router der`          | relación derecha               |
| `izq fouter der`          | ambas relaciones               |

---

### Unión — `union`

Devuelve todas las filas de ambas relaciones. Ambas deben tener las mismas columnas. Los duplicados se eliminan.

```
resultado := r1 union r2;
```

---

### Intersección — `intersect`

Devuelve solo las filas que aparecen en ambas relaciones.

```
resultado := r1 intersect r2;
```

---

### Diferencia — `difference`

Devuelve las filas que están en la primera relación pero no en la segunda.

```
resultado := r1 difference r2;
```

---

### Producto cartesiano — `product`

Devuelve todas las combinaciones de filas de ambas relaciones.

```
resultado := r1 product r2;
```

!!! warning "Resultados grandes"
    Si `r1` tiene 100 filas y `r2` tiene 50, el producto tiene 5.000 filas. Usarlo con cuidado.

---

## Anidamiento de expresiones

Los operadores se pueden anidar libremente:

```
q1 := estudiantes njoin (inscripciones njoin cursos);
q2 := project nombre, nombre_curso (q1);
q3 := select nombre_curso = 'Bases de Datos' (q2);
```

---

## Comentarios

Las líneas que empiezan con `%` son comentarios:

```
% Selecciona todos los estudiantes adultos
adultos := select edad >= 18 (estudiantes);
```

---

## ¿Y la división?

El operador de división no está implementado directamente en Pireal — y es intencional. La división puede expresarse combinando los operadores que ya tenés: producto cartesiano, diferencia y proyección.

Deducir cómo hacerlo es un ejercicio excelente para entender el Álgebra Relacional en profundidad. Si llegás a la solución, significa que realmente entendés cómo funciona.
