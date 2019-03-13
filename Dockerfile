FROM python:3.7.2-stretch

LABEL maintainer="<samatkins@outlook.com>"

ARG PIP_REQUIREMENTS

ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/app
WORKDIR /opt/app
COPY . /opt/app

RUN pip install --upgrade pip
RUN pip install -r /opt/app/$PIP_REQUIREMENTS

EXPOSE 8000
ENV PYTHONPATH=$PYTHONPATH:/opt/app/
