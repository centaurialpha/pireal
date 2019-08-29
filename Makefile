PYTEST = pytest tests

help:
	@echo "test \t\t run tests"
	@echo "test-gui \t run tests for GUI"
	@echo "pep8 \t\t run pycodestyle"
	@echo "flake8 \t run flake8"
	@echo "lint \t\t run pycodestyle and flake8"
	@echo "dist \t\t run python setup.py sdist"
	@echo "deb \t\t build a .deb package"
	@echo "install \t run python setup.py install"

clean:
	rm -rf `find -name "*pyc"`
	rm -rf `find -name "*pyo"`
	rm -rf `find -name "*qmlc"`
	rm -rf .pybuild/
	rm -rf debian/debhelper-build-stamp
	rm -rf debian/files
	rm -rf debian/pireal/
	rm -rf debian/pireal.postinst.debhelper
	rm -rf debian/pireal.prerm.debhelper
	rm -rf debian/pireal.substvars
	rm -rf pireal.egg-info
	rm -rf build/

pep8:
	pycodestyle src

flake8:
	flake8 src -v

lint: pep8 flake8

test:
	@$(PYTEST) -v --cov src.core --cov-report term-missing -m "not gui"

test-gui:
	@$(PYTEST) -v -m gui

dist: clean
	python setup.py sdist
	mv dist/* ../

deb:
	debuild -b -uc -us

install:
	python setup.py install
