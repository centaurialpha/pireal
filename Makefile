PYTEST = pytest tests

help:
	@echo "test 	 		-- run tests"
	@echo "test-gui  		-- run tests for GUI"
	@echo "test-integration 	-- run integration tests"
	@echo "pep8 			-- run pycodestyle"
	@echo "flake8			-- run flake8"
	@echo "lint 			-- run pycodestyle and flake8"
	@echo "dist 			-- run python setup.py sdist"
	@echo "deb 			-- build a .deb package"

clean:
	rm -rf `find -name "*pyc"`
	rm -rf `find -name "*pyo"`
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

test:
	@$(PYTEST) -v --cov pireal.core --cov-report term-missing -m "not integration and not gui" --ignore=tests/gui

test-gui:
	@$(PYTEST) -v -m gui

test-integration:
	@$(PYTEST) -v -m integration --ignore=tests/gui

dist: clean
	python setup.py sdist
	mv dist/* ../

deb:
	debuild -b -uc -us

install:
	python setup.py install
