FROM debian:11
FROM python:3.10.1-slim-buster

WORKDIR /KRISTY/

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get -y install git
RUN python3 -m pip install -U pip
RUN apt-get install -y wget python3-pip curl bash neofetch ffmpeg software-properties-common

COPY requirements.txt .

RUN pip3 install wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt
RUN apt-get update && apt upgrade -y && apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
CMD ["python3", "-m", "KRISTY"]
