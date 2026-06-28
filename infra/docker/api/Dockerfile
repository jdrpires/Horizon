FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3

WORKDIR /app

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml README.md LICENSE ./
COPY services ./services
COPY packages ./packages

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import socket; socket.create_connection(('127.0.0.1', 8000), 2).close()"

CMD ["uvicorn", "horizon_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
