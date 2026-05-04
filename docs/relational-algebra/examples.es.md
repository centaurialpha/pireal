# Ejemplos

Ejemplos prácticos usando la base de datos de ejemplo que viene con Pireal. Podés abrirla desde **Archivo -> Abrir ejemplo** y ejecutar las consultas directamente.

---

## La base de datos

**`alumno`**

| id_alumno | nombre | ciudad       | edad |
|-----------|--------|--------------|------|
| 11        | Juan   | Buenos Aires | 18   |
| 41        | Manuel | Lima         | 16   |
| 01        | Pedro  | Santiago     | 14   |
| 21        | Diego  | Lima         | 12   |
| 31        | Rosita | Concepción   | 15   |

**`curso`**

| cod_curso | nombre_curso             | fecha_inicio | duración | valor |
|-----------|--------------------------|--------------|----------|-------|
| 03547     | Introducción a la POO    | 01/03/2017   | 30       | 4000  |
| 05478     | Machine Learning         | 20/04/2017   | 20       | 5000  |
| 01142     | Python                   | 13/01/2017   | 15       | 4000  |
| 04578     | Programación Funcional   | 05/04/2017   | 10       | 1500  |
| 02145     | Django                   | 15/02/2017   | 12       | 2500  |

**`inscripto`**

| cod_inscripto | id_alumno | cod_curso |
|---------------|-----------|-----------|
| 5             | 41        | 03547     |
| 4             | 21        | 02145     |
| 3             | 11        | 03547     |
| 2             | 01        | 02145     |
| 1             | 01        | 05478     |

---

## Selección básica

Alumnos mayores de 14 años:

```
mayores := select edad > 14 (alumno);
```

Cursos con valor menor a 3000:

```
baratos := select valor < 3000 (curso);
```

Cursos que comienzan después de marzo:

```
tardios := select fecha_inicio > '01/03/2017' (curso);
```

Condiciones combinadas:

```
rango_medio := select valor >= 1500 and valor <= 3000 (curso);
```

---

## Proyección básica

Mostrar solo nombre y ciudad de los alumnos:

```
ubicaciones := project nombre, ciudad (alumno);
```

---

## Selección y proyección combinadas

Nombres de los cursos con valor menor a 3000:

```
q := project nombre_curso (select valor < 3000 (curso));
```

---

## Join natural

Alumnos con los cursos en los que están inscriptos:

```
q1 := alumno njoin inscripto;
q2 := q1 njoin curso;
q3 := project nombre, nombre_curso (q2);
```

---

## Left outer join

Todos los alumnos, incluso los que no están inscriptos en ningún curso:

```
resultado := alumno louter inscripto;
```

Los alumnos sin inscripciones aparecen con `null` en la columna `cod_curso`.

---

## Operaciones de conjunto

```
grupo_a := select ciudad = 'Lima' (alumno);
grupo_b := select edad >= 15 (alumno);
```

**Unión** - alumnos que cumplen cualquiera de las dos condiciones:

```
todos := grupo_a union grupo_b;
```

**Intersección** - alumnos que cumplen ambas condiciones:

```
ambos := grupo_a intersect grupo_b;
```

**Diferencia** - alumnos de Lima que tienen menos de 15 años:

```
solo_a := grupo_a difference grupo_b;
```

---

## Ejemplo completo paso a paso

Nombres de los alumnos inscriptos en cursos que comienzan después de marzo:

```
% Paso 1: cursos que comienzan después de marzo
tardios := select fecha_inicio > '01/03/2017' (curso);

% Paso 2: inscripciones en esos cursos
ins_tardias := inscripto njoin tardios;

% Paso 3: unir con alumnos para obtener nombres
con_nombres := alumno njoin ins_tardias;

% Paso 4: proyectar las columnas relevantes
resultado := project nombre, nombre_curso (con_nombres);
```
