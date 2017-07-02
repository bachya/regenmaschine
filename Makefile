coverage:
	pipenv run codecov
docs:
	cd docs && make html
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
publish:
	python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg regenmaschine.egg-info/
test:
	pipenv run pytest --cov-report term-missing --cov=regenmaschine -s tests/
