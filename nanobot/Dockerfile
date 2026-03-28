ARG REGISTRY_PREFIX_DOCKER_HUB=

FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14-slim-bookworm AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY --from=workspace / /app
WORKDIR /app/nanobot
RUN uv sync --no-dev

FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14-slim-bookworm AS runtime
ARG APP_UID=1000
ARG APP_GID=1000
RUN groupadd -g ${APP_GID} app && useradd -m -u ${APP_UID} -g ${APP_GID} app
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/nanobot/.venv/bin:${PATH}"
WORKDIR /app/nanobot
COPY --from=builder /app /app
RUN chown -R app:app /app
USER app
CMD ["python", "/app/nanobot/entrypoint.py"]
