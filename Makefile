.PHONY: install lint format test coverage run lab docker clean

install:
	poetry install

lint:
	poetry run ruff check .
	poetry run black --check .
	poetry run mypy

format:
	poetry run ruff check . --fix
	poetry run black .

test:
	poetry run pytest

coverage:
	poetry run pytest --cov --cov-report=term-missing --cov-report=xml

run:
	poetry run uvicorn horizon_api.main:app --host 0.0.0.0 --port 8000

lab:
	python apps/horizon-lab/main.py

docker:
	docker compose up --build

clean:
	rm -rf .coverage .mypy_cache .pytest_cache .ruff_cache coverage.xml htmlcov
