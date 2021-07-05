FROM python:3.9.6

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -yq --no-install-recommends apt-utils
RUN apt install -y htop nano && apt update -y
RUN apt install -y curl autoconf automake libtool pkg-config

WORKDIR /img
COPY requirements.txt /img
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
