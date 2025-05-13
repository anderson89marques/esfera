SHELL=/bin/bash


run:
		uv run uvicorn --host 0.0.0.0 src.main:app

test:
	@uv run pytest -svv

test-matching:
	@uv run pytest -svv -k=$(K)

lint:
	ruff check . && blue --check . --diff && isort --check . --diff 

format:
	blue .  && isort .	

migration:
	@uv run alembic revision --autogenerate -m $(name)

migrate:
	@uv run alembic upgrade head

sync:
	@uv sync -v
