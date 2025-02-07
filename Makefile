PROJECT_NAME = gdpr-obfuscator
PYTHON_INTERPRETER=python
WD=$(shell pwd)
PYTHONPATH=${WD}
VENV=venv
PIP=pip
SHELL := /bin/bash

# Create python interpreter environment
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv $(VENV) --python=$(PYTHON_INTERPRETER); \
	)

# Execute python related functionalities from within the project's environment
define execute_in_env
	source venv/bin/activate && $1
endef

# Install dependencies
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

# Install tools for testing and checking
dev-setup: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements-dev.txt)

# Build / Run

## Run the security test (bandit + safety)
security-test: dev-setup
	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the black code check
run-black: dev-setup
	$(call execute_in_env, black  ./obfuscator/*.py ./test/*.py)

## Run the flake8 code check
run-flake8: dev-setup
	$(call execute_in_env, flake8  ./obfuscator/main.py ./obfuscator/csv_utils.py ./test/*.py)

## Run the unit tests
unit-test: requirements
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -vv --testdox)

## Run the coverage check
check-coverage: dev-setup
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} coverage run --omit 'venv/*' -m pytest && coverage report -m)

## Run all checks
run-checks: security-test run-flake8 unit-test check-coverage

### Remove packages
remove-packages:
	rm -r build
	rm -r dist
	rm -r obfuscator.egg-info

## Create package
create-package: dev-setup
	$(call execute_in_env, python setup.py sdist bdist_wheel)


