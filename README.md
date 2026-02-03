### Hexlet tests and linter status:
[![Actions Status](https://github.com/nm01n/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/nm01n/python-project-52/actions)

# Task Manager

[![Deployed on Render](https://img.shields.io/badge/deployed-Render-46E3B7)](https://task-manager-63zz.onrender.com)

🚀 **Live Demo**: https://task-manager-63zz.onrender.com

## Описание
Система управления задачами на Django - учебный проект Hexlet.

## Технологии
- Python 3.10+
- Django 5.2
- PostgreSQL
- Gunicorn
- Whitenoise
- uv (пакетный менеджер)

## Установка локально
```bash
# Клонирование
git clone https://github.com/nm01n/python-project-52.git
cd python-project-52

# Установка зависимостей
make install

# Создание .env файла
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# Миграции
make migrate

# Запуск
make run
```

## Команды Makefile
- `make install` - установка зависимостей
- `make run` - запуск dev-сервера
- `make migrate` - применение миграций
- `make makemigrations` - создание миграций
- `make collectstatic` - сборка статики
- `make lint` - проверка кода линтером
- `make test` - запуск тестов
