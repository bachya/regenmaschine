coverage:
	pipenv run codecov
docs:
	cd docs && make html
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
test:
	pipenv run pytest --cov-report term-missing --cov=regenmaschine -s tests/