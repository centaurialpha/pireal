# Operators

Pireal supports the core operators of Relational Algebra. All queries follow this syntax:

```
result_name := expression;
```

---

## Unary operators

### Selection — `select`

Filters rows that satisfy a condition.

```
result := select condition (relation);
```

**Comparison operators:** `=`, `<>`, `<`, `<=`, `>`, `>=`

**Logical operators** `and` / `or` to combine conditions:

```
result := select age >= 18 and age <= 30 (students);
```

---

### Projection — `project`

Selects specific columns from a relation.

```
result := project col1, col2 (relation);
```

!!! warning "Duplicate elimination"
    Projection automatically eliminates duplicate rows.

---

## Binary operators

### Natural Join — `njoin`

Joins two relations on columns that share the same name.

```
result := left njoin right;
```

---

### Outer Joins

| Syntax              | Keeps unmatched from... |
|---------------------|-------------------------|
| `left louter right` | left relation           |
| `left router right` | right relation          |
| `left fouter right` | both relations          |

---

### Union — `union`

Returns all rows from both relations (same columns required). Duplicates eliminated.

```
result := r1 union r2;
```

---

### Intersection — `intersect`

Returns only rows that appear in both relations.

```
result := r1 intersect r2;
```

---

### Difference — `difference`

Returns rows in the first relation but not the second.

```
result := r1 difference r2;
```

---

### Cartesian Product — `product`

Returns all combinations of rows from both relations.

```
result := r1 product r2;
```

!!! warning "Large results"
    Use with care — results grow multiplicatively.

---

## Nesting expressions

```
q1 := students njoin (enrollments njoin courses);
q2 := project name, course_name (q1);
```

---

## Comments

Lines starting with `%` are comments:

```
% Select all adult students
adults := select age >= 18 (students);
```

---

## What about division?

The division operator isn't implemented in Pireal — and that's intentional. Division can be expressed by combining the operators you already have: cartesian product, difference, and projection.

Figuring out how is a great exercise for understanding Relational Algebra at a deeper level. If you get there, you really get it.
