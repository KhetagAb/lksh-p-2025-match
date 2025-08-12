FROM python:3.11-slim

WORKDIR /app

COPY lkshmatch/requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV MATCH_ENV=prod

CMD ["python", "main.py"]
