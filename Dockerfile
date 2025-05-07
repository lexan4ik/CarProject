# Базовый образ (лучше использовать официальный Python-образ)
FROM python:3.11-slim

# Устанавливаем зависимости для работы с Python и очистки кэша
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория в контейнере
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn --no-cache-dir
# Копируем весь проект в контейнер
COPY . .

# Создание директорий для статики и медиа

## Собираем статические файлы и выполняем миграции (можно через скрипт)
#RUN python manage.py collectstatic --noinput
#RUN python manage.py migrate --noinput

# Порт, который будет слушать контейнер
EXPOSE 8000

# Команда запуска приложения (например, через Gunicorn)
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]