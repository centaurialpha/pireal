<div id="top"></div>

<div align="center">

  # πreal

  [![CI](https://github.com/centaurialpha/pireal/actions/workflows/cicd.yml/badge.svg)](https://github.com/centaurialpha/pireal/actions/workflows/cicd.yml)
  [![Coverage Status](https://coveralls.io/repos/github/centaurialpha/pireal/badge.svg)](https://coveralls.io/github/centaurialpha/pireal)
  ![code style](https://img.shields.io/badge/code%20style-black-black?style=flat)
  [![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
  [![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)

A Relational Algebra interpreter.

  [Getting started](#getting-started) •
  [Report Bug](https://github.com/centaurialpha/pireal/issues)

</div>

<!-- ABOUT THE PROJECT -->
## About The Project
<!--<div align="center">
  <img src="https://user-images.githubusercontent.com/5894606/112898688-89c90680-90b7-11eb-8ae1-372d406b33fd.png" width=70% height=70%>
</div>
-->

**πireal** is a teaching tool for use in learning introduction to database. It allows the user to interactively experiment with Relational Algebra.

<p align="right">(<a href="#top">back to top</a>)</p>

## Demo
<img src="https://user-images.githubusercontent.com/5894606/163731005-6874b4c3-174a-4451-b011-a2a17c8bf521.gif" width=70% height=70%>

### Built With

* [Python](https://python.org/)
* [PyQt](https://riverbankcomputing.com/software/pyqt/intro)
* [Qt](https://www.qt.io/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

You can download the installer from [here](). Currently we only have installer for Windows and Debian. If you know how to pack for Mac OS or any other Linux distribution, I'll thank you.

There is always the option to execute from the sources:

### Prerequisites

**NOTE**: The following commands assume that you have activated the virtual environment of your project.

```
$ pip install .
```

<!-- CONTRIBUTING -->
## Contributing

First install all dependencies to have the development environment ready:

```
$ make pip-install
```
Take a look the `Makefile` for more commands:

```
$ make
test                    -- run tests
test-gui                -- run tests for GUI
test-integration        -- run integration tests
pep8                    -- run pycodestyle
flake8                   -- run flake8
lint                    -- run pycodestyle and flake8
dist                    -- run python setup.py sdist
deb                     -- build a .deb package
rc                      -- buil resources
```

Now you're ready to contribute to the project 🙂.

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU GPLv3. See `COPYING` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Gabriel Acosta - [@_alfacentauri](https://twitter.com/_alfacentauri) - acostadariogabriel@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>
