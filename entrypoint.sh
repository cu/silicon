#!/bin/sh

set -e

export PATH="/$APP_NAME/bin:$PATH"

flask init-db

eval "exec $@"
