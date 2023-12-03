# server/Dockerfile
FROM python:3.9-buster

WORKDIR /app

# 他に必要なパッケージやライブラリがあれば追加

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Pythonコード内でGitの機能を直接呼び出す
RUN pip install GitPython

COPY . /app

CMD ["python", "app.py"]
