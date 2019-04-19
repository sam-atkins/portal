FROM python:3.6.8-stretch

LABEL maintainer="<samatkins@outlook.com>"

ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/app
WORKDIR /opt/app
COPY . /opt/app

ARG PIP_REQUIREMENTS=requirements.txt
RUN python3 -m pip install -r ${PIP_REQUIREMENTS}

EXPOSE 8000
ENV PYTHONPATH=$PYTHONPATH:/opt/app/
