# Queries

Query files (`.pqf`) contain the Relational Algebra expressions you want to evaluate against a database. They're plain text files that you can save, share, and reuse.

---

## Writing queries

Each query is an assignment:

```
result_name := expression;
```

The `:=` assigns the result of the expression to a name. That name then appears in the sidebar and can be used in subsequent expressions.

Multiple queries in the same file are executed in order, top to bottom:

```
q1 := select age >= 18 (students);
q2 := project name (q1);
```

Here `q2` uses `q1`, which is valid because `q1` is defined first.

---

## Running queries

With a database open, press **F5** or go to **Query → Run** to execute all queries in the current file.

Each result opens in a new tab and appears in the left sidebar. You can click any result in the sidebar to inspect it.

!!! warning "A database must be open"
    Queries need a database to run against. Open or create a database before executing queries.

---

## Comments

Use `%` to add comments. Everything after `%` on a line is ignored:

```
% Select students older than 18
adults := select age >= 18 (students);

q := project name (adults);  % only names
```

---

## Error messages

If a query contains an error, Pireal shows a message describing what went wrong. Common errors:

**Undefined relation:**

```
q := select age = 25 (typo);
% Error: Relation 'typo' is not defined
```

**Undefined attribute:**

```
q := project nonexistent (students);
% Error: Attribute 'nonexistent' is not defined in relation 'students'
```

**Duplicate result name:**

```
q := select age = 25 (students);
q := project name (students);
% Error: A result named 'q' already exists
```

Use different names for each query result.

---

## Query file example

A complete `.pqf` file combining multiple operations:

```
% === Student and course analysis ===

% All students enrolled in any course
enrolled := students njoin enrollments;

% Courses cheaper than 3000
affordable := select price < 3000 (courses);

% Students enrolled in affordable courses
q1 := enrolled njoin affordable;
q2 := project name, course_name (q1);

% Courses starting after March (for reference)
late_courses := select start_date > '01/03/2017' (courses);
```

---

## Tips

- Break complex queries into steps with intermediate names — it's easier to debug and understand.
- Use comments to explain what each step does; it helps when reviewing queries later.
- You can re-run queries after modifying the database or the query file without restarting Pireal.

---

## More features

### Syntax tree (AST)

<!-- SCREENSHOT: AST view for a query -->

Pireal can show you the abstract syntax tree it builds internally when parsing your query. It's a concrete way to see how an interpreter "understands" your code — very useful if you're studying Compilers or just curious about how it all works.

### SQL generator

<!-- SCREENSHOT: SQL output panel -->

Every Relational Algebra query has an equivalent in SQL. Pireal can generate it automatically, letting you compare both languages and understand the connection between them.

### Writing the database as code

<!-- SCREENSHOT: .pdb text editor -->

Instead of using the relation creation form, you can write your database directly as plain text. Faster, easier to share, and plays nicely with git.
