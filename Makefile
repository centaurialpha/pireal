clean:
	rm -rf `find -name "*pyc"`
	rm -rf `find -name "*pyo"`
	rm -rf `find -name "*qmlc"`

test:
	pytest -m "not integration" tests --cov src.core.relation --cov src.core.interpreter  --cov src.core.file_manager --cov src.core.cliparser --cov src.core.pfile --cov-report term-missing -s

