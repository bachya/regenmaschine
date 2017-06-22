all: tests docs
tests:
	pytest --cov-report term-missing --cov=regenmaschine -s tests/
docs:
	cd docs && make html
