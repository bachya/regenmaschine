clean:
	pipenv --rm
coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=regenmaschine tests
init:
	pip3 install --upgrade pip pipenv
	pipenv lock
	pipenv install --three --dev
	pipenv run pre-commit install
lint:
	pipenv run flake8 regenmaschine
	pipenv run pydocstyle regenmaschine
	pipenv run pylint regenmaschine
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg regenmaschine.egg-info/
test:
	pipenv run py.test
typing:
	pipenv run mypy --ignore-missing-imports regenmaschine
