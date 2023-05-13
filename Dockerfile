FROM python:3.10.2-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -qq -y \
    build-essential libpq-dev libffi-dev --no-install-recommends git \
    python3-dev python3-setuptools

RUN pip install --upgrade pip

COPY ./req_dev.txt /code/req_dev.txt

RUN pip install -r req_dev.txt

COPY ./entrypoint.sh /code/

COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]

