.PHONY: setup
setup: requirements.txt
	pip3 install -r requirements.txt

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
	rm -rf __pycache__ 
