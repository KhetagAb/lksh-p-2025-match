FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
# RUN apt-get update && apt-get install -y \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/bff

COPY config.toml /app/bff/config.toml

# RUN mkdir -p /app/bff/lkshmatch/webapp/templates
# COPY lkshmatch/webapp/templates/ /app/bff/lkshmatch/webapp/templates/

ENV PYTHONPATH=/app
ENV MATCH_ENV=prod

EXPOSE 8000

# Команда для запуска приложения
# Можно выбрать один из вариантов запуска:
# 1. Только веб-приложение
# CMD ["uvicorn", "lkshmatch.webapp.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 2. Только телеграм бот
CMD ["python", "-m", "bff.lkshmatch.main"]

# 3. Веб-приложение (по умолчанию)
# CMD ["uvicorn", "lkshmatch.webapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
