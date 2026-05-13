PYTEST = pytest tests

help:
	@echo "test 	 			-- run tests"
	@echo "test-unit 	 		-- run unit tests"
	@echo "test-interpreter		-- run tests for Scanner, Lexer, Parser and Interpreter"
	@echo "test-integration 	-- run integration tests"

rc:
	pyrcc5 pireal/resources/resources.qrc -o pireal/resources.py

clean:
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

check:
	uv run ruff check

test-unit:
	uv run pytest -v tests/unit -m "not interpreter"

test-interpreter:
	uv run pytest -v -m interpreter --cov=pireal.interpreter --cov-report term-missing

test-integration:
	uv run pytest -v tests/integration -s

test: test-unit test-integration

deb:
	debuild -b -uc -us
