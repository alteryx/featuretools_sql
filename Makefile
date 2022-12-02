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
	pip freeze | grep -v "alteryx/featuretools_sql.git" | grep -E $(allow_list) > $(OUTPUT_PATH)


.PHONY: package
package: upgradepip upgradebuild upgradesetuptools
	python -m build
	$(eval PACKAGE=$(shell python -c "from pep517.meta import load; metadata = load('.'); print(metadata.version)"))
	tar -zxvf "dist/featuretools_sql-${PACKAGE}.tar.gz"
	mv "featuretools_sql-${PACKAGE}" unpacked_sdist
