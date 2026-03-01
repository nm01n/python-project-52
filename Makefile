.PHONY: install
install:
	uv sync --system

.PHONY: migrate
migrate:
	uv run python manage.py migrate

.PHONY: collectstatic
collectstatic:
	uv run python manage.py collectstatic --no-input

.PHONY: run
run:
	uv run python manage.py runserver

.PHONY: shell
shell:
	uv run python manage.py shell

.PHONY: makemigrations
makemigrations:
	uv run python manage.py makemigrations

.PHONY: createsuperuser
createsuperuser:
	uv run python manage.py createsuperuser

.PHONY: lint
lint:
	uv run ruff check code

.PHONY: test
test:
	uv run python manage.py test

.PHONY: build
build:
	./build.sh

.PHONY: render-start
render-start:
	uv run gunicorn hexlet_code.wsgi:application

.PHONY: setup
setup:
	uv sync
	uv run python manage.py migrate

.PHONY: start-server
start-server:
	uv run python manage.py runserver 0.0.0.0:3000
