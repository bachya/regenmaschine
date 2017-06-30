init:
	pip install pipenv
	pipenv lock
	pipenv install --dev
coverage:
	pipenv run codecov --token=41f0313d-f147-4eb0-b571-df8929bc1314
docs:
	cd docs && make html
test:
	pipenv run pytest --cov-report term-missing --cov=regenmaschine -s tests/
travis: test coverage
