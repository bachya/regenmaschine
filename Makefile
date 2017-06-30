docs:
	cd docs && make html
init:
	pip install pipenv
	pipenv lock
	pipenv install --dev
test:
	pipenv run pytest --cov-report term-missing --cov=regenmaschine -s tests/
upload_coverage:
	pipenv run codecov --token=41f0313d-f147-4eb0-b571-df8929bc1314
