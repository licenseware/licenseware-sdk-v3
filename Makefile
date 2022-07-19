
run-tests:
	coverage run --source=licenseware -m pytest tests/test_* 
	coverage html 
	coverage report -m 
	rm coverage.svg
	coverage-badge -o coverage.svg


build:
	python3 setup.py bdist_wheel sdist
	rm -rf build


install:
	pip3 uninstall -y licenseware
	python3 setup.py bdist_wheel sdist
	rm -rf build
	pip3 install dist/licenseware-3.0.0-py3-none-any.whl

uninstall:
	pip3 uninstall -y licenseware


