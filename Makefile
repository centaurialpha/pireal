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
test:
	pytest -v tests --cov src.core.relation --cov src.core.interpreter  --cov src.core.file_manager --cov src.core.cliparser --cov src.core.pfile --cov-report term-missing -m "not testgui"

test-gui:
	pytest -v tests -m testgui

dist: clean
	python setup.py sdist
	mv dist/* ../

deb:
	debuild -b -uc -us

install:
	python3 setup.py install
