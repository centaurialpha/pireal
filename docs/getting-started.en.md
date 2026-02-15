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

There's no macOS installer yet. If you're on a Mac and know how to package Python apps, your contribution would be very welcome! Open an [issue on GitHub](https://github.com/centaurialpha/pireal/issues) and we'll coordinate.

### From source

On any platform, with [uv](https://docs.astral.sh/uv/) installed:

```bash
git clone https://github.com/centaurialpha/pireal
cd pireal
uv run pireal
```

---

## First steps

When you open Pireal for the first time, you'll see three panels:

- **Left sidebar** — shows the relations in your database and query results
- **Top area** — the database view, where you see and edit your relations
- **Bottom editor** — where you write your Relational Algebra queries

### 1. Open the example database

Go to **File → Open example** to load a pre-built database. This is the fastest way to start writing queries without creating anything from scratch.

### 2. Create your own database

Go to **File → New Database**. Define relations using the text syntax in the editor:

```
students(id, name, age)
1, Gabriel, 25
2, Marisel, 30
3, Rodrigo, 25
```

### 3. Write your first query

```
q := select age = 25 (students);
```

Press **F5** to execute. The result appears in the sidebar and opens in a new tab.

### 4. Chain operations

```
young := select age < 30 (students);
names := project name (young);
```

---

## Keyboard shortcuts

| Action            | Shortcut        |
|-------------------|-----------------|
| Run queries       | `F5`            |
| New database      | `Ctrl+N`        |
| Open file         | `Ctrl+O`        |
| Save file         | `Ctrl+S`        |
| Toggle dark mode  | `Ctrl+Shift+D`  |

---

## Next steps

- Learn all the available [operators](relational-algebra/operators.md)
- See practical [examples](relational-algebra/examples.md)
- Read about [database files](user-guide/databases.md)
