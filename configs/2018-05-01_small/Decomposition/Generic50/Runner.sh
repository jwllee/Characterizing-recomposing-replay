#!/usr/bin/env bash

cd prom-6.5.1

PYTHON=python
RUN=../src/decompose/decomposer.py
DECOMPOSERCONFIGS=../configs/2018-05-01_small/Decomposition/Generic50/Decomposer\ configs.json
LOGGINGCONFIGS=../src/logging.json

# variables containing spaces need to be surrounded with double quotes so that
# they are passed as one single variable!
$PYTHON $RUN -c "${DECOMPOSERCONFIGS}" -l "${LOGGINGCONFIGS}"
