ARG APP_NAME=silicon
ARG PYTHON_IMAGE=python:3.10-slim
ARG NODE_IMAGE=node:17-alpine

# Staging:
# * copy the project dir into /staging
# * install the javascript dependencies
FROM $NODE_IMAGE AS staging

COPY ./ /staging/
WORKDIR /staging/silicon/static

RUN npm install


# Build:
# * run tests
# * build a wheel and constraints file
# * create a venv in /$APP_NAME
# * install wheel and dependencies into the venv
FROM $PYTHON_IMAGE AS build
ARG APP_NAME
ENV PYTHONUNBUFFERED=1

COPY --from=staging /staging /staging
WORKDIR /staging

RUN pip install --no-cache-dir poetry
RUN poetry install
RUN TMP=/dev/shm poetry run pytest
RUN poetry build --format wheel
RUN poetry export --format requirements.txt --output constraints.txt --without-hashes

RUN python -m venv /$APP_NAME
RUN /$APP_NAME/bin/pip install dist/*.whl --constraint constraints.txt


# Final stage:
# * create a user named $APP_NAME
# * install curl and set healthcheck
# * create an instance data directory
FROM $PYTHON_IMAGE AS final

ARG APP_NAME
ENV APP_NAME=$APP_NAME
ENV FLASK_APP=$APP_NAME:create_app()
ENV INSTANCE_PATH=/home/$APP_NAME/instance
ENV GUNICORN_CMD_ARGS="--bind :5000 --workers 2 --threads 4"

COPY --from=build /$APP_NAME /$APP_NAME
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -yq --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
HEALTHCHECK --start-period=10s --timeout=5s \
    CMD curl http://localhost:5000/view/home || exit 1

RUN groupadd --gid 5000 $APP_NAME
RUN useradd --create-home --uid 5000 --gid 5000 $APP_NAME

USER $APP_NAME
WORKDIR /home/$APP_NAME

RUN mkdir instance

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--worker-tmp-dir /dev/shm", "$FLASK_APP"]
