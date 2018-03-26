#!/usr/bin/env bash

cd prom-6.5.1

PYTHON=python
RUN=../src/experiments/run.py
REPLAYCONFIGSRECO=../configs/default/Default\ recomposing\ replayer\ configs.json
REPLAYCONFIGSMONO=../configs/default/Default\ monolithic\ replayer\ configs.json
LOGGINGCONFIGS=../src/logging.json

# variables containing spaces need to be surrounded with double quotes so that
# they are passed as one single variable!
$PYTHON $RUN -c "${REPLAYCONFIGSRECO}" -l "${LOGGINGCONFIGS}"
$PYTHON $RUN -c "${REPLAYCONFIGSMONO}" -l "${LOGGINGCONFIGS}"