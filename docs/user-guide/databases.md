# Databases

A Pireal database (`.pdb` file) is a plain text file that defines one or more relations. You can create it from the graphical interface or write it directly with any text editor.

---

## File format

Each relation starts with a header line that defines the name and columns, followed by one row per line:

```
@relation_name:col1,col2,col3
value1,value2,value3
value4,value5,value6
```

A complete database with multiple relations:

```
@students:id,name,age
1,Gabriel,25
2,Marisel,30
3,Rodrigo,25

@courses:course_id,course_name,price
10,Databases,2500
20,Networks,3500
30,Python,1500

@enrolled:id,course_id
1,10
1,30
2,20
```

!!! note "Header format"
    The relation name is preceded by `@` and separated from the columns by `:`. Columns are separated by `,` with no spaces.

---

## Creating a database

### From the interface

Go to **File -> New database**. An editor opens where you can write the database using the text syntax. When you save, Pireal writes the `.pdb` file.

### With the new relation dialog

Go to **Database -> New relation** to open a form where you can define columns and enter rows without writing the syntax manually.

### Opening an existing file

Go to **File -> Open** and select a `.pdb` file. Recent files also appear under **File -> Recent**.

---

## Editing relations

You can edit the database content directly in the editor. Changes take effect when you save.

!!! note "Unsaved changes indicator"
    When a database has unsaved changes, the tab shows a `*` before the filename. Use `Ctrl+S` to save.

---

## Data types

All values are stored as text, but Pireal interprets them correctly when comparing in a query:

| Type    | Examples                          |
|---------|-----------------------------------|
| Numbers | `25`, `3500`, `3.14`              |
| Strings | `'Gabriel'`, `'Databases'`        |
| Dates   | `'15/03/2017'`, `'2024-01-01'`    |
| Times   | `'10:30'`, `'23:59'`              |

When comparing in a `select` condition, strings and dates go in single quotes:

```
result := select name = 'Gabriel' (students);
result := select start_date > '01/03/2017' (courses);
```

Numbers are compared without quotes:

```
result := select price >= 2000 (courses);
```

---

## Sample database

Pireal includes a ready-to-use sample database. Open it from **File -> Open example** to explore an academic scenario with students, courses and enrollments, without creating anything from scratch.
