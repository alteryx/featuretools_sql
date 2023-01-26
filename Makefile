.PHONY: clean
clean:
	find . -name '*.pyo' -delete
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	find . -name '*~' -delete
	find . -name '.coverage.*' -delete

.PHONY: installdeps
installdeps:
	pip install -e .

.PHONY: installdeps-dev
installdeps-dev:
	pip install -e ".[dev]"
	pre-commit install

.PHONY: installdeps-test
installdeps-test:
	pip install -e ".[test]"

.PHONY: lint
lint:
	black . --config=./pyproject.toml --check
	ruff . --config=./pyproject.toml

.PHONY: lint-fix
lint-fix:
	black . --config=./pyproject.toml --check
	ruff . --config=./pyproject.toml --fix

.PHONY: test
test:
	pytest featuretools_sql/tests/*

.PHONY: upgradepip
upgradepip:
	python -m pip install --upgrade pip

.PHONY: upgradebuild
upgradebuild:
	python -m pip install --upgrade build

.PHONY: upgradesetuptools
upgradesetuptools:
	python -m pip install --upgrade setuptools

.PHONY: checkdeps
checkdeps:
	$(eval allow_list='numpy|pandas|featuretools|psycopg2|sqlalchemy|PyMySQL|snowflake-sqlalchemy[pandas]')
	pip freeze | grep -v "alteryx/featuretools_sql" | grep -E $(allow_list) > $(OUTPUT_PATH)

.PHONY: package
package: upgradepip upgradebuild upgradesetuptools
	python -m build
	$(eval PACKAGE=$(shell python -c 'import setuptools; setuptools.setup()' --version))
	tar -zxvf "dist/featuretools_sql-${PACKAGE}.tar.gz"
	mv "featuretools_sql-${PACKAGE}" unpacked_sdist
