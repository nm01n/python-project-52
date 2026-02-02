install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --no-input

run:
	uv run python manage.py runserver

shell:
	uv run python manage.py shell

makemigrations:
	uv run python manage.py makemigrations

createsuperuser:
	uv run python manage.py createsuperuser

lint:
	uv run flake8 task_manager

test:
	uv run python manage.py test

build:
	./build.sh

render-start:
	uv run gunicorn hexlet-code.wsgi:application
