WORKDIR := $(shell pwd)

PORT?=8000


help: ## Display help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

run_all: ## Run db + app
	docker compose up

run_app: ## Run application
	docker compose up app

run_migrate: ## Run migrate
	docker compose exec app ./manage.py migrate

make_migrate: ## Make migrate
	docker compose exec app ./manage.py makemigrations

make_super_user: ## Make super user
	docker compose exec app ./manage.py createsuperuser


open_shell: ## Open shell to the app container
	docker compose exec app bash

run_test: ## Run test
	docker compose exec app bash -c  "DJANGO_SETTINGS_MODULE=test_task.test_settings ./manage.py test"