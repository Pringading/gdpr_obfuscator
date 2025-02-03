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

# CHECKS
## Install Bandit - finds common security issues
bandit: create-environment
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety: create-environment
	$(call execute_in_env, $(PIP) install safety)

## Install flake8
flake8: create-environment
	$(call execute_in_env, $(PIP) install flake8)

## Install black
black: create-environment
	$(call execute_in_env, $(PIP) install black)

## Install coverage
coverage: create-environment
	$(call execute_in_env, $(PIP) install coverage)

## Set up dev requirements (bandit, safety, black)
dev-setup: bandit safety black coverage
	$(call execute_in_env, $(PIP) install -r ./dev-requirements.txt)

# Build / Run

## Run the security test (bandit + safety)
security-test: safety bandit
	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, bandit -lll */*.py *c/*/*.py)

## Run the black code check
run-black: black
	$(call execute_in_env, black  ./src/*.py ./test/*.py)

## Run the flake8 code check
run-flake8: flake8
	$(call execute_in_env, flake8  ./src/*.py ./test/*.py)

## Run the unit tests
unit-test: requirements
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} pytest -vv --testdox)

## Run the coverage check
check-coverage: coverage
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH} coverage run --omit 'venv/*' -m pytest && coverage report -m)

## Run all checks
run-checks: security-test run-flake8 run-black unit-test coverage


