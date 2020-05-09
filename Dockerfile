FROM python:3.7-alpine
MAINTAINER Jorge Bueno

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev


RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN wget http://www.sqlite.org/2017/sqlite-autoconf-3170000.tar.gz
RUN tar xvfz sqlite-autoconf-3170000.tar.gz
RUN apk add --update alpine-sdk
RUN ./sqlite-autoconf-3170000/configure --prefix=/usr
RUN make
RUN make install
RUN rm sqlite-autoconf-3170000.tar.gz

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user