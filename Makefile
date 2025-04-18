.PHONY: sync
sync:
	uv sync --all-extras

.PHONY: lint
lint: 
	uv run ruff check

.PHONY: mypy
mypy: 
	uv run mypy --strict .

.PHONY: tests
tests: 
	uv run pytest 
