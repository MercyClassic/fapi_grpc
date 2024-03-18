FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTEDECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/src

COPY ./pyproject.toml /app/pyproject.toml

RUN apt update \
    && pip install poetry \
    && apt install -y libmagic1 \
    && apt install -y curl \
    && useradd -U app \
    && chown -R app:app /app \
    && chdir /app \
    && poetry config virtualenvs.create false \
    && poetry install --only main

WORKDIR /app/src

COPY --chown=app:app . /app

EXPOSE 8000

USER app

CMD ["sh", "/app/entrypoint.sh"]
