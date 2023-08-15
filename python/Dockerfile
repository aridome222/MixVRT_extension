FROM python:3.9-buster

RUN pip install selenium==4.10.0 pytest Pillow Selenium-Screenshot 
RUN pip install beautifulsoup4 
RUN pip install matplotlib
RUN apt update -y && apt upgrade -y
RUN apt install -y python3-dev python3-pip python3-setuptools
RUN apt-get install -y libgl1-mesa-dev
RUN python3 -m pip install --upgrade pip setuptools
RUN python3 -m pip install scikit-build
RUN yes 1 | python3 -m pip install opencv-python