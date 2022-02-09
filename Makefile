lint:
	poetry run python3 -m pylint ./pavo

static:
	poetry run python3 -m mypy ./pavo

test:
	poetry run python3 -m pytest --cov=./pavo tests/