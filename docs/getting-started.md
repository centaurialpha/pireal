# Getting Started

## Installation

### Windows

Download the installer from the [releases page](https://github.com/centaurialpha/pireal/releases) and follow the steps. Next, next, finish.

### Linux

Download the AppImage from the [releases page](https://github.com/centaurialpha/pireal/releases):

```bash
chmod +x Pireal-x86_64.AppImage
./Pireal-x86_64.AppImage
```

### macOS

There is no macOS installer yet. If you use a Mac and know how to package Python apps, your contribution would be very welcome. Open an [issue on GitHub](https://github.com/centaurialpha/pireal/issues) and we can coordinate.

### From source

On any platform, with [uv](https://docs.astral.sh/uv/) installed:

```bash
git clone https://github.com/centaurialpha/pireal
cd pireal
uv run pireal
```

---

## The interface

When you first open Pireal you will see the start screen with shortcuts to create or open a database. Once you open one, three panels appear:

- **Left sidebar** - shows the database relations and query results
- **Top panel** - the database view, where you see and edit your relations
- **Bottom editor** - where you write your Relational Algebra queries

---

## 1. Open the sample database

Go to **File -> Open example** to load a pre-built database. It is the fastest way to start writing queries without creating anything from scratch.

The example includes relations like `student`, `course` and `enrolled` - a classic academic scenario.

---

## 2. Create your own database

Go to **File -> New database**. You can define relations using the text syntax directly in the editor:

```
@students:id,name,age
1,Gabriel,25
2,Marisel,30
3,Rodrigo,25
```

Each relation starts with `@name:col1,col2,...` followed by one row per line.

!!! note "File extensions"
    Pireal databases are saved as `.pdb`. Query files use `.pqf`.

---

## 3. Write your first query

In the bottom query editor, write:

```
q := select age = 25 (students);
```

Press **F5** (or **Query -> Run**) to execute. The result appears in the sidebar and opens in a new tab.

---

## 4. Chain operations

Queries can be nested and assigned to names:

```
young    := select age < 30 (students);
names    := project name (young);
```

Each assignment creates a new result you can inspect independently.

---

## Keyboard shortcuts

| Action            | Shortcut       |
|-------------------|----------------|
| Run queries       | `F5`           |
| New database      | `Ctrl+N`       |
| Open file         | `Ctrl+O`       |
| Save file         | `Ctrl+S`       |
| Dark mode         | `Ctrl+Shift+D` |

---

## Next steps

- Learn all the available [operators](relational-algebra/operators.md)
- See practical [examples](relational-algebra/examples.md) with real queries
- Read about [database files](user-guide/databases.md) and the syntax in detail
