all: tests docs
tests:
	pytest --cov=regenmaschine tests/
docs:
	cd docs && make html
