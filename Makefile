PYTEST = pytest tests

help:
	@echo "test 	 		-- run tests"
	@echo "test-gui  		-- run tests for GUI"
	@echo "test-integration 	-- run integration tests"
	@echo "flake8			-- run flake8"
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

flake8:
	flake8 src/pireal --config=.flake8

format-check:
	@black src/ tests/ --check

format:
	@black src/ tests/

test-unit:
	pytest -v tests/unit --cov pireal --cov-report term-missing

test-gui:
	@$(PYTEST) -v -m gui

test-integration:
	pytest -v tests/integration -s

test: test-unit test-integration

dist: clean
	python setup.py sdist
	mv dist/* ../

deb:
	debuild -b -uc -us

install:
	python setup.py install

pip-install:
	@pip install -r requirements.txt -r requirements-dev.txt

pip-compile:
	@rm -f requirements*.txt
	@pip-compile requirements.in
	@pip-compile requirements-dev.in

pip-sync:
	@pip-sync requirements*.txt
