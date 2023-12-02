# server/Dockerfile
FROM python:3.9-buster

WORKDIR /app

# 他に必要なパッケージやライブラリがあれば追加

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app.py"]
