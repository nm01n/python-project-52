.PHONY: install
install:
	uv sync --system

.PHONY: setup
setup:
	cd code && uv sync
	cd code && uv run python manage.py migrate

.PHONY: migrate
migrate:
	cd code && uv run python manage.py migrate

.PHONY: makemigrations
makemigrations:
	cd code && uv run python.manage.py makemigrations

.PHONY: collectstatic
collectstatic:
	cd code && uv run python manage.py collectstatic --no-input

.PHONY: run
run:
	cd code && uv run python manage.py runserver

.PHONY: start-server
start-server:
	cd code && uv run python manage.py runserver 0.0.0.0:3000

.PHONY: shell
shell:
	cd code && uv run python manage.py shell

.PHONY: createsuperuser
createsuperuser:
	cd code && uv run python manage.py createsuperuser

.PHONY: test
test:
	cd code && uv run python manage.py test

.PHONY: lint
lint:
	uv lint

.PHONY: render-start
render-start:
	cd code && uv run python /venv/bin/gunicorn hexlet_code.wsgi:application

.PHONY: build
build:
	./build.sh
