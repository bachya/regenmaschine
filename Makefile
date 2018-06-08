ci:
	pipenv run py.test --junitxml=report.xml
coverage:
	pipenv run py.test --verbose --cov-report term-missing --cov-report xml --cov=regenmaschine tests
docs:
	cd docs && make html
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
lint:
	pipenv run pylint regenmaschine
	pipenv run flake8 regenmaschine
	pipenv run pydocstyle regenmaschine
publish:
	python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg regenmaschine.egg-info/
test:
	pipenv run detox
