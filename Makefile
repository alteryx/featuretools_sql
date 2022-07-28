.PHONY: setup
setup: requirements.txt
	pip3 install -r requirements.txt

.PHONY: lint
lint:
	isort --check-only featuretools-sql
	black featuretools-sql -t py310 --check
	flake8 featuretools-sql

.PHONY: lint-fix
lint-fix:
	black featuretools-sql -t py310 
	isort featuretools-sql 

.PHONY: test
test: 
	pytest -s -vv featuretools-sql/tests/* 

.PHONY: clean
clean: 
	rm -rf __pycache__ 
