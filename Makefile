# Makefile для проекта Django с uv

.PHONY: install
install:
	cd code && uv sync --system

.PHONY: migrate
migrate:
	uv run python code/manage.py migrate

.PHONY: makemigrations
makemigrations:
	uv run python code/manage.py makemigrations

.PHONY: collectstatic
collectstatic:
	uv run python code/manage.py collectstatic --no-input

.PHONY: run
run:
	uv run python code/manage.py runserver

.PHONY: shell
shell:
	uv run python code/manage.py shell

.PHONY: createsuperuser
createsuperuser:
	uv run python code/manage.py createsuperuser

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: test
test:
	uv run python code/manage.py test

.PHONY: build
build:
	./build.sh

.PHONY: render-start
render-start:
	uv run gunicorn hexlet_code.wsgi:application

.PHONY: setup
setup: install migrate

.PHONY: start-server
start-server:
	uv run python code/manage.py runserver 0.0.0.0:3000
