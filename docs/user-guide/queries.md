# Queries

Query files (`.pqf`) contain the Relational Algebra expressions to evaluate against an open database. They are plain text files you can save, share and reuse.

---

## Writing queries

Each query is an assignment:

```
result_name := expression;
```

The `:=` assigns the result of the expression to a name. That name appears in the sidebar and can be used in subsequent expressions.

Multiple queries in the same file are executed in order, top to bottom:

```
q1 := select age >= 18 (students);
q2 := project name (q1);
```

---

## Running queries

With a database open, press **F5** or go to **Query -> Run**.

!!! warning "A database must be open"
    Queries need a database to run against. Open or create one before executing.

---

## Comments

Use `%` to add comments:

```
% Select students older than 18
adults := select age >= 18 (students);

q := project name (adults);  % names only
```

---

## Error messages

If a query has an error, Pireal shows a descriptive message. Some common examples:

**Undefined relation:**

```
q := select age = 25 (typo);
% Error: relation 'typo' is not defined
```

**Undefined attribute:**

```
q := project nonexistent (students);
% Error: attribute 'nonexistent' is not defined in relation 'students'
```

**Duplicate result name:**

```
q := select age = 25 (students);
q := project name (students);
% Error: a result named 'q' already exists
```

---

## Extra features

### Syntax tree (AST)

Pireal can show you the tree it builds internally when parsing your query. It's a concrete way to see how an interpreter "understands" your code, great if you're studying Compilers or just curious about how things work.

Enable it from **Query -> View AST**.

### SQL generator

Every Relational Algebra query has an equivalent in SQL. Pireal can generate it automatically so you can compare both languages and understand how they relate.

Enable it from **Query -> Generate SQL**.

---

## Terminal mode

If you prefer working from the command line, Pireal has a REPL mode that runs without a graphical interface:

```bash
pireal --terminal my_database.pdb
```

If you omit the file, Pireal will ask for it on startup.

Once inside, you write queries just like in the interface, ending with `;` to execute:

```
pireal> q := select age >= 18 (students);
```

Results are displayed directly in the terminal. Multi-line queries work too, Pireal waits until it finds the `;`:

```
pireal> q := project name (
     …      select age >= 18 (students)
     …  );
```

**Available commands:**

| Command      | Action                              |
|--------------|-------------------------------------|
| `\h`         | Show help                           |
| `\r`         | List loaded relations               |
| `\r name`    | Show the contents of a relation     |
| `exit` / `quit` / `:q` | Exit                   |

---

## Tips

- Break complex queries into steps with intermediate names, easier to understand and debug.
- Use comments to explain what each step does.
- You can re-run queries after modifying the database without restarting Pireal.
