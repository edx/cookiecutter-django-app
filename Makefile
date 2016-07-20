.PHONY: bake help pip-compile quality replay requirements test validate watch

BAKE_OPTIONS=--no-input

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

bake: ## generate project using defaults
	cookiecutter $(BAKE_OPTIONS) . --overwrite-if-exists

pip-compile: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip-compile -o requirements/base.txt requirements/base.in
	pip-compile -o requirements/dev.txt requirements/dev.in
	pip-compile -o requirements/doc.txt requirements/doc.in
	pip-compile -o requirements/test.txt requirements/test.in
	pip-compile -o requirements/travis.txt requirements/travis.in

quality: ## check coding style with pycodestyle and pylint
	tox -e quality

replay: BAKE_OPTIONS=--replay
replay: watch ## replay last cookiecutter run and watch for changes
	;

requirements: ## install development environment requirements
	pip install -qr requirements/dev.txt --exists-action w
	pip-sync requirements/base.txt requirements/dev.txt requirements/private.* requirements/test.txt

test: ## run tests on every supported Python version
	tox

validate: ## run tests and quality checks
	tox -e quality,py27,py35

watch: bake ## generate project using defaults and watch for changes
	watchmedo shell-command -p '*.*' -c 'make bake -e BAKE_OPTIONS=$(BAKE_OPTIONS)' -W -R -D \{{cookiecutter.repo_name}}/
