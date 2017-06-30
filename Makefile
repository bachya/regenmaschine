init:
	pip install pipenv
	pipenv lock
	pipenv install --dev
test:
	pytest --cov-report term-missing --cov=regenmaschine -s tests/
docs:
	cd docs && make html
