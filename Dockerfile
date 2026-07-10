# Stage 1: builder
FROM python:3.14-slim AS builder

ENV POETRY_VERSION=2.0.0 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY pyproject.toml ./
RUN poetry install --only main --no-root

# Stage 2: runtime
FROM python:3.14-slim

RUN groupadd -r app && useradd -r -g app -d /app -s /bin/false app

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini .
RUN mkdir logs && chown app:app logs

EXPOSE 8000

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
