FROM python:3.11-slim-buster

ENV APP_HOME=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache


LABEL maintainer='knimako84@gmail.com'
LABEL description="Development image for PAPSS Project"


RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y python3-dev libpq-dev libpq5 python3-venv \
    && apt-get install -y gettext \
    && apt-get install -y netcat-openbsd gcc default-libmysqlclient-dev pkg-config libmagic-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install poetry==1.7.1


WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock ./

RUN mkdir $APP_HOME/staticfiles

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install && rm -rf $POETRY_CACHE_DIR

COPY ./docker/local/django/entrypoint /entrypoint

RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower



ENTRYPOINT [ "/entrypoint" ]