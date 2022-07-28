# syntax=docker/dockerfile:1

FROM python:3.9 

ARG POETRY_VERSION

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /car-indicators

COPY poetry.lock /car-indicators/
COPY pyproject.toml /car-indicators/

RUN poetry config  virtualenvs.create false \
    && poetry install $(test "$TYPE_PROJECT_ENV" == production) --no-interaction --no-ansi

COPY ./car_indicators /car-indicators/car_indicators/



