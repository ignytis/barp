#!/usr/bin/env sh

docker run \
    --rm \
    -v $PWD:/app \
    -w /app \
    python:3.13-alpine \
        sh /app/tests/functional/_runner.sh