#!/usr/bin/env bash
# Exit on error
set -o errexit

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем зависимости
make install

# Собираем статику
make collectstatic

# Применяем миграции
make migrate
