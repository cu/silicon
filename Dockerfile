ARG PYTHON_IMAGE=docker.io/library/python:3.13-slim
ARG NODE_IMAGE=docker.io/library/node:lts-alpine

### Stage 1: Install JS dependencies
FROM $NODE_IMAGE AS npm-install

COPY ./ /staging/
WORKDIR /staging/silicon/static
RUN npm ci

### Stage 2: Install Silicon and dependencies
FROM $PYTHON_IMAGE AS build

# uv settings
ARG UV_LINK_MODE=copy
ARG UV_COMPILE_BYTECODE=1
ARG UV_PYTHON_DOWNLOADS=never
ARG UV_PROJECT_ENVIRONMENT=/silicon/.venv

COPY --from=npm-install /staging /staging
WORKDIR /staging

RUN --mount=type=cache,target=/root/.cache <<EOS sh -ex
    pip install uv
    uv sync --locked --no-install-project
    TMP=/dev/shm uv run pytest
    mv LICENSE scripts silicon /silicon
    mv entrypoint.sh /
EOS

### Stage 3: Configure final image
FROM $PYTHON_IMAGE AS final

ENV FLASK_APP=silicon:create_app()
ENV INSTANCE_PATH=/home/silicon/instance
ENV GUNICORN_CMD_ARGS="--bind :5000 --workers 2 --threads 4"

COPY --from=build /entrypoint.sh /
RUN chmod +x /entrypoint.sh
COPY --from=build /silicon /silicon

ARG DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked <<EOS sh -ex
    apt-get update
    apt-get install -yq --no-install-recommends curl tini
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    groupadd --gid 5000 silicon
    useradd --create-home --uid 5000 --gid 5000 silicon
EOS
USER silicon
WORKDIR /silicon

EXPOSE 5000
HEALTHCHECK --start-period=10s --timeout=5s \
    CMD curl http://localhost:5000/view/home || exit 1
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
CMD ["/silicon/.venv/bin/gunicorn", "--worker-tmp-dir /dev/shm", "'silicon:create_app()'"]
