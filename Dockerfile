# Базовий образ — Python 3.12 slim (легкий, швидкий, безпечний)
FROM python:3.12-slim

# Встановлюємо системні залежності (потрібні для деяких pip-пакетів)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Робоча директорія
WORKDIR /app

# Спочатку залежності — для кешування шару
COPY requirements.txt .

# Встановлюємо пакети без кешу (менший розмір образу)
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir uvicorn[standard] httptools uvloop

# Копіюємо весь код
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Запуск Uvicorn у production-режимі
# workers = 4 (можна динамічно через env)
# --no-access-log — зменшує логи
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--no-access-log"]