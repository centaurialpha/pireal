PYTEST = pytest tests

help:
	@echo "test \t\t run tests"
	@echo "test-gui \t run tests for GUI"
	@echo "test-integration \t run integration tests"
	@echo "pep8 \t\t run pycodestyle"
	@echo "flake8 \t run flake8"
	@echo "lint \t\t run pycodestyle and flake8"
	@echo "pipeline \t run all kind of tests and lints"
	@echo "dist \t\t run python setup.py sdist"
	@echo "deb \t\t build a .deb package"
	@echo "install \t run python setup.py install"

clean:
	rm -rf `find -name "*pyc"`
	rm -rf `find -name "*pyo"`
	rm -rf `find -name "*qmlc"`
	rm -rf .pybuild/
	rm -rf debian/debhelper-build-stamp
	rm -rf debian/.debhelper
	rm -rf debian/files
	rm -rf debian/pireal/
	rm -rf debian/pireal.postinst.debhelper
	rm -rf debian/pireal.prerm.debhelper
	rm -rf debian/pireal.substvars
	rm -rf pireal.egg-info
	rm -rf build/

pep8:
	pycodestyle pireal

flake8:
	flake8 pireal

lint: pep8 flake8

mypy:
	mypy pireal --ignore-missing-imports

test:
	@$(PYTEST) -v --cov pireal.core --cov-report term-missing -m "not integration and not gui" --ignore=tests/gui

test-gui:
	@$(PYTEST) -v -m gui

test-integration:
	@$(PYTEST) -v -m integration --ignore=tests/gui

pipeline: lint test test-gui test-integration

dist: clean
	python setup.py sdist
	mv dist/* ../

deb:
	debuild -b -uc -us

install:
	python setup.py install
