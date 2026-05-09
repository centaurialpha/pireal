# Examples

Practical examples using the sample database that comes with Pireal. Open it from **File -> Open example** and run the queries directly.

---

## The database

**`student`**

| student_id | name   | city         | age |
|------------|--------|--------------|-----|
| 11         | Juan   | Buenos Aires | 18  |
| 41         | Manuel | Lima         | 16  |
| 01         | Pedro  | Santiago     | 14  |
| 21         | Diego  | Lima         | 12  |
| 31         | Rosita | Concepción   | 15  |

**`course`**

| course_id | course_name            | start_date | duration | price |
|-----------|------------------------|------------|----------|-------|
| 03547     | Intro to OOP           | 01/03/2017 | 30       | 4000  |
| 05478     | Machine Learning       | 20/04/2017 | 20       | 5000  |
| 01142     | Python                 | 13/01/2017 | 15       | 4000  |
| 04578     | Functional Programming | 05/04/2017 | 10       | 1500  |
| 02145     | Django                 | 15/02/2017 | 12       | 2500  |

**`enrolled`**

| enrollment_id | student_id | course_id |
|---------------|------------|-----------|
| 5             | 41         | 03547     |
| 4             | 21         | 02145     |
| 3             | 11         | 03547     |
| 2             | 01         | 02145     |
| 1             | 01         | 05478     |

---

## Basic selection

Students older than 14:

```
older := select age > 14 (student);
```

Courses with a price below 3000:

```
affordable := select price < 3000 (course);
```

Courses starting after March:

```
late := select start_date > '01/03/2017' (course);
```

Combined conditions:

```
mid_range := select price >= 1500 and price <= 3000 (course);
```

---

## Basic projection

Show only name and city of students:

```
locations := project name, city (student);
```

---

## Selection and projection combined

Names of courses with a price below 3000:

```
q := project course_name (select price < 3000 (course));
```

---

## Natural join

Students with the courses they are enrolled in:

```
q1 := student njoin enrolled;
q2 := q1 njoin course;
q3 := project name, course_name (q2);
```

---

## Left outer join

All students, even those not enrolled in any course:

```
result := student louter enrolled;
```

Students with no enrollments appear with `null` in the `course_id` column.

---

## Set operations

```
group_a := select city = 'Lima' (student);
group_b := select age >= 15 (student);
```

**Union** - students that meet either condition:

```
all := group_a union group_b;
```

**Intersection** - students that meet both conditions:

```
both := group_a intersect group_b;
```

**Difference** - students from Lima who are under 15:

```
only_a := group_a difference group_b;
```

---

## Full step-by-step example

Names of students enrolled in courses that start after March:

```
% Step 1: courses starting after March
late_courses := select start_date > '01/03/2017' (course);

% Step 2: enrollments in those courses
late_enrollments := enrolled njoin late_courses;

% Step 3: join with students to get names
with_names := student njoin late_enrollments;

% Step 4: project the relevant columns
result := project name, course_name (with_names);
```

---

## Division

Which students are enrolled in **every** available course?

```
% Project only the (student, course) pairs
enrollments  := project id_alumno, cod_curso (inscripto);

% The full set of courses
all_courses  := project cod_curso (curso);

% Students present in every course
result := enrollments divide all_courses;
```

The result contains only the `id_alumno` values that are paired with **every** `cod_curso` in `enrollments`. If a student is missing even one course, they are excluded
