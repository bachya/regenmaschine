coverage:
	codecov --token=41f0313d-f147-4eb0-b571-df8929bc1314
docs:
	cd docs && make html
init:
	pip install pipenv
	pipenv install --dev
prod: test coverage
test:
	pytest --cov-report term-missing --cov=regenmaschine -s tests/
