[![Linux Tests](https://github.com/centaurialpha/pireal/actions/workflows/test-linux.yml/badge.svg)](https://github.com/centaurialpha/pireal/actions/workflows/test-linux.yml)
[![Windows Tests](https://github.com/centaurialpha/pireal/actions/workflows/test-windows.yml/badge.svg)](https://github.com/centaurialpha/pireal/actions/workflows/test-windows.yml)
[![Coverage Status](https://coveralls.io/repos/github/centaurialpha/pireal/badge.svg)](https://coveralls.io/github/centaurialpha/pireal)
---

**πireal** is a teaching tool for use in learning introduction to database. It allows the user to interactively experiment with Relational Algebra.

| Home Page | In action |
|:--------:|:----------:|
| ![pireal-screenshot](https://user-images.githubusercontent.com/5894606/112898694-8b92ca00-90b7-11eb-8515-cf04649f11f9.png) | ![pireal-in-action](https://user-images.githubusercontent.com/5894606/112898688-89c90680-90b7-11eb-8ae1-372d406b33fd.png) |

#### Platforms
- GNU/Linux
- Windows
- Mac OS X

### Requirements to run/install from source
- [Python 3](http://python.org/)
- [PyQt5](http://www.riverbankcomputing.co.uk/software/pyqt/intro)
- PyQt5 Qt Quick Module (package `python3-pyqt5.qtquick` in Debian)

### Implemented Operators
The operations are implemented in [relation.py](https://github.com/centaurialpha/pireal/blob/master/src/core/relation.py).

|Operator|Supported|
|--------|---------|
| Selection | :heavy_check_mark: |
| Projection | :heavy_check_mark: |
| Rename | :x: |
| Product | :heavy_check_mark: |
| Union | :heavy_check_mark: |
| Difference | :heavy_check_mark: |
| Intersection | :heavy_check_mark: |
| Natural Join | :heavy_check_mark: |
| Left Outer Join | :heavy_check_mark: |
| Right Outer Join | :heavy_check_mark: |
| Full Outer Join | :heavy_check_mark: |
| Division | :x: |

### Donate

I have developed Pireal with a lot of :heart:, I hope it is useful.

You can donate any amount that you think Pireal deserves.

[![donar](https://www.paypalobjects.com/es_XC/AR/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=29STPF8BWWUTY)

|  Author |
|---|
| [Gabriel Acosta](https://centaurialpha.github.io)  |
