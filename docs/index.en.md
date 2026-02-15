# πireal

**Pireal** is a free and open source Relational Algebra interpreter designed for learning database fundamentals. It lets you create relations, write Relational Algebra queries, and see the results instantly — no SQL, no setup, no noise.

Perfect for students and teachers exploring how databases work under the hood.

---

## Why Pireal?

Most database courses jump straight to SQL. Pireal takes a step back and lets you work directly with **Relational Algebra** — the mathematical foundation that SQL is built on. Understanding this layer makes SQL (and databases in general) click in a way that's hard to achieve otherwise.

With Pireal you can:

- Write Relational Algebra queries and see the results instantly in an interactive table
- **Visualize relations** — explore the structure and data of each relation in the sidebar
- **Inspect the syntax tree (AST)** — Pireal can show you the tree it builds internally when parsing your query, great for understanding how an interpreter works
- **Generate equivalent SQL** — every query can be automatically translated to SQL so you can compare both languages
- **Write your database as code** — define relations as plain text, no forms needed
- Compare multiple results side by side
- Load example databases to get started quickly

---

## Quick Example

Given a relation `students`:

| id | name    | age |
|----|---------|-----|
| 1  | Gabriel | 25  |
| 2  | Marisel | 30  |
| 3  | Rodrigo | 25  |

This query selects students aged 25 and shows only their names:

```
q := project name (select age = 25 (students));
```

Result:

| name    |
|---------|
| Gabriel |
| Rodrigo |

---

## Installation

Download the installer from the [releases page](https://github.com/centaurialpha/pireal/releases), or run from source with [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/centaurialpha/pireal
cd pireal
uv run pireal
```

For more installation options, see [Getting Started](getting-started.md).
