.PHONY: install
install:
	cd code && uv sync --system

.PHONY: migrate
migrate:
	cd code && uv run python manage.py migrate

.PHONY: collectstatic
collectstatic:
	cd code && uv run python manage.py collectstatic --no-input

.PHONY: run
run:
	cd code && uv run python manage.py runserver

.PHONY: shell
shell:
	cd code && uv run python manage.py shell

.PHONY: makemigrations
makemigrations:
	cd code && uv run python manage.py makemigrations

.PHONY: createsuperuser
createsuperuser:
	cd code && uv run python manage.py createsuperuser

.PHONY: lint
lint:
	cd code && uv run ruff check .

.PHONY: test
test:
	cd code && uv run python manage.py test

.PHONY: build
build:
	./build.sh

.PHONY: render-start
render-start:
	cd code && uv run gunicorn hexlet_code.wsgi:application

.PHONY: setup
setup: install migrate

.PHONY: start-server
start-server:
	cd code && uv run python manage.py runserver 0.0.0.0:3000
