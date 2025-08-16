FROM python:3.11-slim

WORKDIR /webapp

COPY lkshmatch/requirements.txt ./

RUN pip install --no-cache-dir --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

ENV PYTHONPATH=/webapp
ENV MATCH_ENV=prod

CMD ["python", "mainWebapp.py"]
