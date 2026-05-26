.PHONY: install extract-idealista extract-ine pipeline-idealista pipeline-ine query lint test

install:
	pip install -e ".[dev]"

extract-idealista:
	python -m src.cli extract idealista

extract-ine:
	python -m src.cli extract ine

pipeline-idealista:
	python -m src.cli pipeline idealista

pipeline-ine:
	python -m src.cli pipeline ine

query:
	@read -p "SQL> " sql && python -m src.cli query "$$sql"

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

format:
	ruff format src/ tests/

test:
	pytest tests/ -v
