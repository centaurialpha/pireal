# Examples

Practical examples using a classic academic database. All examples use these relations:

**`students`** — enrolled students

| id | name    | guardian        |
|----|---------|-----------------|
| 1  | Gabriel | Ana Acosta      |
| 2  | Marisel | Carlos Pereyra  |
| 3  | Rodrigo | Hector Fuentes  |

**`courses`** — available courses

| course_id | course_name | price | start_date   |
|-----------|-------------|-------|--------------|
| 10        | Databases   | 2500  | 15/03/2017   |
| 20        | Networking  | 3500  | 10/04/2017   |
| 30        | Python      | 1500  | 01/02/2017   |

**`enrollments`** — which student is enrolled in which course

| id | course_id |
|----|-----------|
| 1  | 10        |
| 1  | 30        |
| 2  | 20        |

---

## Basic selection

Get all courses cheaper than 3000:

```
cheap := select price < 3000 (courses);
```

Get courses that start after March:

```
late := select start_date > '01/03/2017' (courses);
```

Combine conditions with `and`:

```
mid_range := select price >= 1500 and price <= 3000 (courses);
```

---

## Basic projection

Show only names and prices of all courses:

```
catalog := project course_name, price (courses);
```

---

## Selection + projection

Show names of courses cheaper than 3000:

```
q1 := select price < 3000 (courses);
q2 := project course_name (q1);
```

Or in one expression:

```
result := project course_name (select price < 3000 (courses));
```

---

## Natural join

Get the full name of each student alongside their guardian:

```
q := students njoin guardians;
```

Get all students with the courses they're enrolled in:

```
q1 := students njoin (enrollments njoin courses);
q2 := project name, course_name (q1);
```

---

## Left outer join

Show all students, including those not enrolled in any course:

```
result := students louter enrollments;
```

Students without enrollments will appear with `null` in the `course_id` column.

---

## Set operations

Given two groups of students:

```
group_a := select id = 1 or id = 2 (students);
group_b := select id = 2 or id = 3 (students);
```

**Union** — all students from either group:

```
everyone := group_a union group_b;
```

**Intersection** — students in both groups:

```
both := group_a intersect group_b;
```

**Difference** — students in group_a but not in group_b:

```
only_a := group_a difference group_b;
```

---

## Putting it all together

Find the names of students enrolled in courses starting after March:

```
% Step 1: courses that start after March
late_courses := select start_date > '01/03/2017' (courses);

% Step 2: join enrollments with those courses
late_enrollments := enrollments njoin late_courses;

% Step 3: join with students to get names
with_names := students njoin late_enrollments;

% Step 4: project only the relevant columns
result := project name, course_name (with_names);
```
