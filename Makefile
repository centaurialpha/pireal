clean:
	rm -rf `find -name "*pyc"`
	rm -rf `find -name "*pyo"`
	rm -rf `find -name "*qmlc"`

test:
	pytest -m "not integration" tests --cov src.core.relation --cov src.core.interpreter  --cov src.core.file_manager --cov src.core.cliparser --cov src.core.pfile --cov-report term-missing -s

dist: clean
	rm -rf /tmp/pireal/
	mkdir /tmp/pireal/
	cp -R * /tmp/pireal/
	(cd /tmp; tar -zcf pireal.tar.gz pireal/)
	mv /tmp/pireal.tar.gz ./pireal_`./pireal --version`.orig.tar.gz
