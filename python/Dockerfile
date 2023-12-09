FROM python:3.9-buster

# sudoとtzdataをインストール
RUN apt-get update && apt-get install -y sudo tzdata

# Dockerfile内でユーザーとグループを設定
RUN useradd -m -s /bin/bash aridome
RUN usermod -aG sudo aridome

# pythonで画像処理を行うのに必要
RUN pip install selenium==4.10.0 pytest Pillow Selenium-Screenshot 
RUN pip install matplotlib
RUN apt update -y && apt upgrade -y
RUN apt install -y python3-dev python3-pip python3-setuptools
RUN apt-get install -y libgl1-mesa-dev
RUN python3 -m pip install --upgrade pip setuptools
RUN python3 -m pip install scikit-build
RUN yes 1 | python3 -m pip install opencv-python

# pngからsvg、svgからpngに変換する際に必要
RUN pip install aspose-words
RUN pip install svgwrite
RUN pip install svglib
RUN pip install reportlab
RUN pip install pdf2image
RUN apt-get update
RUN apt-get install -y poppler-utils

# スクレイングするのに必要
RUN pip install beautifulsoup4 
RUN pip install lxml
RUN pip install regex

# Tesseract-OCRに必要
RUN sudo apt-get install -y tesseract-ocr
RUN sudo apt-get install tesseract-ocr-jpn
RUN sudo apt-get install tesseract-ocr-eng
RUN pip install pytesseract

# Azure-ComputerVisionに必要
RUN pip install azure-cognitiveservices-vision-computervision

# Azure-OCRに必要
RUN pip install azure-ai-formrecognizer

# フォントをコピーしてパスを設定
COPY ./MSMINCHO.TTC /usr/share/fonts/MSMINCHO.TTC
ENV FONT_PATH=/usr/share/fonts/MSMINCHO.TTC

# CORS (Cross-Origin Resource Sharing)を許可する設定を追加する
RUN pip install flask_cors

# # Seleniumによる自動操作されているWeb画面の録画に必要
# RUN sudo apt-get update && \
#     sudo apt-get install -y ffmpeg
