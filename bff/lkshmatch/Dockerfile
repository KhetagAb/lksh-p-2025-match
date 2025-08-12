# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY lkshmatch/requirements.txt ./

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Копируем весь код проекта
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV MATCH_ENV=prod

# Команда для запуска телеграм бота
CMD ["python", "main.py"]
