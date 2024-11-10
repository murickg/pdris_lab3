FROM python:3.11-slim

# Обновляем apt и устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get install -y libpq-dev curl gnupg build-essential && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Обновляем pip
RUN python -m pip install --upgrade --no-cache-dir pip

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
