# πreal 

> A free and open source Relational Algebra interpreter for learning databases.

[![CI](https://github.com/centaurialpha/pireal/actions/workflows/cicd.yml/badge.svg)](https://github.com/centaurialpha/pireal/actions/workflows/cicd.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org)
[![PyQt6](https://img.shields.io/badge/PyQt-6-green)](https://www.riverbankcomputing.com/software/pyqt/)

Pireal lets you create relations, write Relational Algebra queries, and see
results instantly, no SQL, no setup, no noise. Built for students and teachers
who want to understand how databases actually work under the hood.

---
 
## The origin story
 
Pireal was born in 2015 out of necessity. Back then the standard tool for
practicing Relational Algebra in university courses was WinRDBI, a Windows-only
application. The problem: I've been a Linux user my whole life, and when I took
my databases course I simply couldn't use it.
 
Instead of dual-booting into Windows like a normal person, I wrote Pireal.
Ten years later it's still here, still cross-platform, and WinRDBI is still
Windows-only.
 
---

## What is this
 
Most database courses jump straight to SQL and skip the theory entirely. Pireal
takes a step back and lets you work directly with Relational Algebra, the
mathematical foundation that SQL is built on. Once this clicks, SQL clicks.
 
You write queries like:
 
```
young := select age < 30 (students);
names := project name (young);
```
 
Hit F5, see the results. That's it.
 
---
 
## Features
 
- All core RA operators: `select`, `project`, `njoin`, `union`, `intersect`,
  `difference`, `product`, outer joins
- Symbol mode: write `σ`, `π`, `⋈` instead of keywords if you're feeling
  fancy (or your professor insists)
- AST viewer: inspect the syntax tree Pireal builds when parsing your query,
  useful if you're also taking a compilers course
- SQL generator: translates any RA query to equivalent SQL so you can compare
  both languages side by side
- Custom themes: drop a JSON file in `~/.pireal/themes/` and it shows up
  automatically
- Plain text `.pdb` database files, readable by humans and version control
  alike
 
---
 
## Installation
 
### Windows
 
Download the installer from the
[releases page](https://github.com/centaurialpha/pireal/releases) and follow
the steps. Next, next, finish.
 
### Linux
 
Download the AppImage from the
[releases page](https://github.com/centaurialpha/pireal/releases):
 
```bash
chmod +x Pireal-x86_64.AppImage
./Pireal-x86_64.AppImage
```
 
### From source
 
Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).
 
```bash
git clone https://github.com/centaurialpha/pireal
cd pireal
uv run pireal
```
 
---
 
## Documentation
 
Full docs, operator reference, examples and a theme creation guide at
[centaurialpha.github.io/pireal](https://centaurialpha.github.io/pireal).
 
---
 
## Contributing
```bash
uv sync --group dev
uvx pre-commit install
uv run pytest
```

Bug reports, fixes, and feature ideas are welcome. Open an issue or send a PR.

---

## License

GNU GPLv3. See `COPYING`.
