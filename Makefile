.PHONY: setup
setup: requirements.txt
	pip3 install -r requirements.txt

.PHONY: lint
lint:
	isort --check-only featuretools-sql
	black featuretools-sql/* --check
	flake8 featuretools-sql

.PHONY: lint-fix
lint-fix:
	black featuretools-sql/* 
	isort featuretools-sql/* 

.PHONY: clean
clean: 
	rm -rf __pycache__ 
