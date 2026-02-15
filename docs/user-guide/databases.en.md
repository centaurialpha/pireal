# Databases

A Pireal database (`.pdb` file) is a plain text file that defines one or more relations. You can create and edit them directly in the Pireal interface or with any text editor.

---

## File format

Each relation starts with a header line defining the name and columns, followed by one row per line:

```
relation_name(col1, col2, col3)
value1, value2, value3
value4, value5, value6
```

A complete database file with multiple relations looks like this:

```
students(id, name, age)
1, Gabriel, 25
2, Marisel, 30
3, Rodrigo, 25

courses(course_id, course_name, price)
10, Databases, 2500
20, Networking, 3500
30, Python, 1500

enrollments(id, course_id)
1, 10
1, 30
2, 20
```

---

## Creating a database

### Using the interface

Go to **File → New Database**. An editor opens where you can type the database using the text syntax above. When you save it, Pireal writes the `.pdb` file.

### Using the Relation Creator dialog

Go to **Database → New Relation** to open a form-based dialog where you can define column names and enter rows without writing the syntax manually.

### Opening an existing file

Go to **File → Open** and select a `.pdb` file.

---

## Editing relations

You can edit the raw database text directly in the editor. Changes take effect after saving the file and reloading the database.

!!! note "Unsaved changes indicator"
    When a database has unsaved changes, the tab shows a `*` before the filename. Use `Ctrl+S` to save.

---

## Data types

All values in Pireal are stored as text internally, but the interpreter handles comparisons correctly for:

| Type    | Examples                                 |
|---------|------------------------------------------|
| Numbers | `25`, `3500`, `3.14`                     |
| Strings | `'Gabriel'`, `'Databases'`               |
| Dates   | `'15/03/2017'`, `'2024-01-01'`           |
| Times   | `'10:30'`, `'23:59:00'`                  |

When comparing values in a `select` condition, quote strings and dates with single quotes:

```
result := select name = 'Gabriel' (students);
result := select start_date > '01/03/2017' (courses);
```

Numbers can be compared without quotes:

```
result := select price >= 2000 (courses);
```

---

## Example database

Pireal ships with a built-in example database. Open it via **File → Open example** to see a ready-to-use academic scenario with students, courses, and enrollments.
