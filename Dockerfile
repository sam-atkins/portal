FROM python:3.6.8-stretch

LABEL maintainer="<samatkins@outlook.com>"

ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/app
WORKDIR /opt/app
COPY . /opt/app

RUN pip install pipenv
RUN pipenv install --system --dev --ignore-pipfile

EXPOSE 8000
ENV PYTHONPATH=$PYTHONPATH:/opt/app/
