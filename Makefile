.PHONY: setup
setup: requirements.txt
	pip3 install -r requirements.txt

.PHONY: lint
lint:
	isort --check-only sequeltools
	black sequeltools -t py310 --check
	flake8 sequeltools

.PHONY: lint-fix
lint-fix:
	black -t py310 sequeltools
	isort sequeltools

.PHONY: clean
clean: 
	rm -rf __pycache__ 