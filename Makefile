.PHONY: install
install:
	uv sync --system


.PHONY: setup
setup:
	uv sync
	/venv/bin/python manage.py migrate


.PHONY: migrate
migrate:
	/venv/bin/python manage.py migrate


.PHONY: makemigrations
makemigrations:
	/venv/bin/python manage.py makemigrations


.PHONY: collectstatic
collectstatic:
	/venv/bin/python manage.py collectstatic --no-input


.PHONY: run
run:
	/venv/bin/python manage.py runserver


.PHONY: start-server
start-server:
	/venv/bin/python manage.py runserver 0.0.0.0:3000


.PHONY: shell
shell:
	/venv/bin/python manage.py shell


.PHONY: createsuperuser
createsuperuser:
	/venv/bin/python manage.py createsuperuser


.PHONY: test
test:
	/venv/bin/python manage.py test


.PHONY: lint
lint:
	/venv/bin/ruff check code


.PHONY: render-start
render-start:
	/venv/bin/gunicorn hexlet_code.wsgi:application


.PHONY: build
build:
	./build.sh
