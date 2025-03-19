FROM python:3.12-slim


# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода приложения
COPY . .



CMD ["python", "run.py"]

