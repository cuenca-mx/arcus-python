SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON=python3.7


all: test

install-dev:
		pip install -q -e .[dev]

venv:
		$(PYTHON) -m venv --prompt arcus venv
		source venv/bin/activate
		pip install --quiet --upgrade pip

test: clean install-dev lint
		python setup.py test

coverage: clean install-dev lint
		coverage run --source=arcus setup.py test
		coverage report -m

lint:
		pycodestyle setup.py arcus/ tests/

clean:
		find . -name '*.pyc' -exec rm -f {} +
		find . -name '*.pyo' -exec rm -f {} +
		find . -name '*~' -exec rm -f {} +
		rm -rf build dist arcus.egg-info

release: clean
		python setup.py sdist bdist_wheel
		twine upload dist/*


.PHONY: all install-dev release test clean-pyc