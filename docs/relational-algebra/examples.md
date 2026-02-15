# Ejemplos

Ejemplos prácticos usando una base de datos académica clásica.

**`estudiantes`**

| id | nombre  | apoderado       |
|----|---------|-----------------|
| 1  | Gabriel | Ana Acosta      |
| 2  | Marisel | Carlos Pereyra  |
| 3  | Rodrigo | Hector Fuentes  |

**`cursos`**

| id_curso | nombre_curso | valor | fecha_inicio |
|----------|--------------|-------|--------------|
| 10       | Bases de Datos | 2500 | 15/03/2017 |
| 20       | Redes        | 3500  | 10/04/2017   |
| 30       | Python       | 1500  | 01/02/2017   |

**`inscripto`**

| id | id_curso |
|----|----------|
| 1  | 10       |
| 1  | 30       |
| 2  | 20       |

---

## Selección básica

Cursos con valor menor a 3000:

```
baratos := select valor < 3000 (cursos);
```

Cursos que comienzan después de marzo:

```
tardios := select fecha_inicio > '01/03/2017' (cursos);
```

Condiciones combinadas:

```
rango_medio := select valor >= 1500 and valor <= 3000 (cursos);
```

---

## Proyección básica

Mostrar solo nombre y valor de los cursos:

```
catalogo := project nombre_curso, valor (cursos);
```

---

## Selección + proyección

Nombres de cursos con valor menor a 3000:

```
q := project nombre_curso (select valor < 3000 (cursos));
```

---

## Join natural

Estudiantes con los cursos en los que están inscriptos:

```
q1 := estudiantes njoin (inscripto njoin cursos);
q2 := project nombre, nombre_curso (q1);
```

---

## Left outer join

Todos los estudiantes, incluso los que no están inscriptos en ningún curso:

```
resultado := estudiantes louter inscripto;
```

Los estudiantes sin inscripciones aparecen con `null` en la columna `id_curso`.

---

## Operaciones de conjunto

```
grupo_a := select id = 1 or id = 2 (estudiantes);
grupo_b := select id = 2 or id = 3 (estudiantes);
```

**Unión** — todos los estudiantes de cualquiera de los grupos:

```
todos := grupo_a union grupo_b;
```

**Intersección** — estudiantes en ambos grupos:

```
ambos := grupo_a intersect grupo_b;
```

**Diferencia** — estudiantes en grupo_a pero no en grupo_b:

```
solo_a := grupo_a difference grupo_b;
```

---

## Ejemplo completo paso a paso

Nombres de los estudiantes inscriptos en cursos que comienzan después de marzo:

```
% Paso 1: cursos que comienzan después de marzo
cursos_tardios := select fecha_inicio > '01/03/2017' (cursos);

% Paso 2: inscripciones en esos cursos
inscripciones_tardias := inscripto njoin cursos_tardios;

% Paso 3: unir con estudiantes para obtener nombres
con_nombres := estudiantes njoin inscripciones_tardias;

% Paso 4: proyectar las columnas relevantes
resultado := project nombre, nombre_curso (con_nombres);
```
