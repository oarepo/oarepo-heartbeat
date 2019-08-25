#!/usr/bin/env bash

isort -rc -c -df **/*.py && \
check-manifest --ignore ".travis-*" && \
python setup.py test
