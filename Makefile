lint:
	poetry run python3 -m pylint ./pavo

static:
	poetry run python3 -m mypy ./pavo

test:
	poetry run python3 -m pytest tests/

cov:
	poetry run python3 -m pytest --cov=./pavo tests/

style:
	poetry run python3 -m black --check pavo