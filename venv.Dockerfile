FROM python:3.7
RUN apt-get update && apt-get install

RUN pip3 install virtualenv

WORKDIR /src
