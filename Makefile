# Makefile для проекта Django + Hexlet/uv

# Устанавливаем зависимости в виртуальное окружение
.PHONY: install
install:
	uv sync --system

# Применяем миграции базы данных
.PHONY: migrate
migrate:
	uv run python code/manage.py migrate

# Создаём статические файлы
.PHONY: collectstatic
collectstatic:
	uv run python code/manage.py collectstatic --no-input

# Запускаем Django сервер
.PHONY: run
run:
	uv run python code/manage.py runserver

# Запускаем Django shell
.PHONY: shell
shell:
	uv run python code/manage.py shell

# Создаём миграции
.PHONY: makemigrations
makemigrations:
	uv run python code/manage.py makemigrations

# Создаём суперпользователя
.PHONY: createsuperuser
createsuperuser:
	uv run python code/manage.py createsuperuser

# Проверяем код с помощью ruff
.PHONY: lint
lint:
	uv run ruff check code

# Запускаем тесты
.PHONY: test
test:
	uv run python code/manage.py test

# Собираем проект (если есть build.sh)
.PHONY: build
build:
	./build.sh

# Запуск через Gunicorn
.PHONY: render-start
render-start:
	uv run gunicorn hexlet_code.wsgi:application

# Полная настройка окружения + миграции
.PHONY: setup
setup:
	$(MAKE) install
	uv run python code/manage.py migrate

# Запуск сервера на всех интерфейсах
.PHONY: start-server
start-server:
	uv run python code/manage.py runserver 0.0.0.0:3000
