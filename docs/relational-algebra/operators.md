# Operators

Pireal supports the core operators of Relational Algebra. All queries follow this syntax:

```
result_name := expression;
```

---

## Unary operators

They take a single relation as input.

### Selection - `select`

Filters the rows that satisfy a condition. Returns a relation with the same columns but only the rows that meet the criteria.

```
result := select condition (relation);
```

**Example:**

```
adults := select age >= 18 (student);
```

**Comparison operators:**

| Operator | Meaning       |
|----------|---------------|
| `=`      | equal         |
| `<>`     | not equal     |
| `<`      | less than     |
| `<=`     | less or equal |
| `>`      | greater than  |
| `>=`     | greater or equal |

**Logical operators** `and`/`or` to combine conditions:

```
result := select age >= 18 and age <= 30 (student);
```

**Comparing strings and dates:**

```
result := select name = 'Juan' (student);
result := select start_date > '01/03/2017' (course);
```

---

### Projection - `project`

Selects specific columns from a relation.

```
result := project col1, col2 (relation);
```

**Example:**

```
names := project name (student);
```

!!! warning "Duplicate elimination"
    Projection automatically removes duplicate rows, since relations are sets.

---

## Binary operators

They take two relations as input.

### Natural Join - `njoin`

Joins two relations on the columns that share the same name. Only includes rows where the shared column values match in both relations.

```
result := left njoin right;
```

**Example:**

```
result := student njoin enrolled;
```

---

### Outer Joins

Like the natural join, but keep the rows without a match, filling missing values with `null`.

| Syntax           | Keeps unmatched rows from... |
|------------------|------------------------------|
| `left louter right` | left relation             |
| `left router right` | right relation            |
| `left fouter right` | both relations            |

**Example:**

```
% All students, even those not enrolled in any course
result := student louter enrolled;
```

---

### Union - `union`

Returns all rows from both relations. Both must have exactly the same columns - same names and same order. Duplicates are removed.

```
result := r1 union r2;
```

---

### Intersection - `intersect`

Returns only the rows that appear in both relations.

```
result := r1 intersect r2;
```

---

### Difference - `difference`

Returns the rows that are in the first relation but not in the second.

```
result := r1 difference r2;
```

---

### Cartesian product - `product`

Returns all possible combinations of rows from both relations.

```
result := r1 product r2;
```

!!! warning "Large results"
    If `r1` has 100 rows and `r2` has 50, the product has 5,000 rows. Use with care.

---

## Nesting expressions

Operators can be freely nested:

```
q1 := student njoin (enrolled njoin course);
q2 := project name, course_name (q1);
q3 := select course_name = 'Python' (q2);
```

---

## Comments

Lines starting with `%` are comments:

```
% Select all adult students
adults := select age >= 18 (student);
```

---

## ~~What about division?~~

~~The division operator is not directly implemented in Pireal, and that is intentional. Division can be expressed by combining the operators you already have: cartesian product, difference and projection.~~

~~Figuring out how to do it is an excellent exercise for understanding Relational Algebra in depth. If you get to the solution, it means you truly understand how it works.~~

!!! success "Update: division is now implemented"
    Turns out the exercise was so good we implemented it. See below.

### Division - `divide`

Returns all tuples from the **left** relation (projected onto the columns not in the right relation) such that they are combined with **every** tuple in the right relation and the combination exists in the left relation.

In practical terms: find every value in R that is "paired with all" values in S.

```
result := dividend divide divisor;
```

**Preconditions:**

- The divisor columns must be a subset of the dividend columns.
- The dividend must have at least one column that is not in the divisor.

**Example:**

Find all students enrolled in every available course:

```
enrollments  := project student_id, course_id (enrolled);
all_courses  := project course_id (course);
in_all       := enrollments divide all_courses;
```

**Unicode symbol:** `÷` can be used instead of `divide`:

```
in_all := enrollments ÷ all_courses;
```

!!! note "Result columns"
    The result contains only the columns from the dividend that are **not** present in the divisor. In the example above, the result has only `student_id`.
