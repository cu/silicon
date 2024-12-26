#!/bin/sh

set -e

export PATH="/silicon/.venv/bin:$PATH"

flask --app silicon init-db

eval "exec $@"
