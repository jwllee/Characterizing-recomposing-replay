#!/usr/bin/env bash

cd prom-6.5.1

PYTHON=python
RUN=../src/experiments/run.py
REPLAYCONFIGSMONO=../configs/BayesianConf/Replay/Monolithic/Monolithic\ replayer\ configs.json
LOGGINGCONFIGS=../src/logging.json

# variables containing spaces need to be surrounded with double quotes so that
# they are passed as one single variable!
$PYTHON $RUN -c "${REPLAYCONFIGSMONO}" -l "${LOGGINGCONFIGS}"

# repeat experiment x2
# $PYTHON $RUN -c "${REPLAYCONFIGSMONO}" -l "${LOGGINGCONFIGS}"

cd ..
