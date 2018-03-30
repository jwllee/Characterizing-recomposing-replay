#!/usr/bin/env bash

cd prom-6.5.1

PYTHON=python
RUN=../src/preprocess/clean.py
DATACLEANERCONFIGS=../configs/DataCleaner/Data\ cleaner\ configs.json
LOGGINGCONFIGS=../src/logging.json

# variables containing spaces need to be surrounded with double quotes so that
# they are passed as one single variable!
$PYTHON $RUN -c "${DATACLEANERCONFIGS}" -l "${LOGGINGCONFIGS}"
