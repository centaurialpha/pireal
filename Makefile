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
	@echo "rc                       -- buil resources"

rc:
	pyrcc5 pireal/resources/resources.qrc -o pireal/resources.py

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
	pycodestyle src/pireal

flake8:
	flake8 src/pireal

lint: pep8 flake8

test-unit:
	pytest -v tests/unit --cov pireal.core --cov-report term-missing

test-interpreter:
	pytest -v tests/interpreter --cov pireal.interpreter --cov-report term-missing

test-gui:
	@$(PYTEST) -v -m gui

test-integration:
	pytest -v tests/integration -s

test: test-unit test-interpreter test-integration

dist: clean
	python setup.py sdist
	mv dist/* ../

deb:
	debuild -b -uc -us

install:
	python setup.py install
