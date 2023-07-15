#!/bin/sh

set -e

export PATH="/$APP_NAME/bin:$PATH"

flask --app $APP_NAME init-db

eval "exec $@"
