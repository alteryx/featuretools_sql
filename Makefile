.PHONY: installdeps
installdeps:
	pip install -e .

.PHONY: installdeps-dev
installdeps-dev:
	pip install -e ".[dev]"

.PHONY: installdeps-test
installdeps-test:
	pip install -e ".[test]"

.PHONY: lint
lint:
	isort --check-only featuretools_sql
	black featuretools_sql -t py310 --check
	flake8 featuretools_sql

.PHONY: lint-fix
lint-fix:
	black featuretools_sql -t py310
	isort featuretools_sql

.PHONY: test
test:
	pytest featuretools_sql/tests/*

.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete
	find . -name '.coverage.*' -delete
