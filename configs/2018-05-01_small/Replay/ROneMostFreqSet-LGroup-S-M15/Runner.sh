#!/usr/bin/env bash

cd prom-6.5.1

PYTHON=python
RUN=../src/experiments/run.py
REPLAYCONFIGSRECO=../configs/2018-05-01_small/Replay/ROneMostFreqSet-LGroup-S-M15/Recomposing\ replayer\ configs.json
LOGGINGCONFIGS=../src/logging.json

# variables containing spaces need to be surrounded with double quotes so that
# they are passed as one single variable!
$PYTHON $RUN -c "${REPLAYCONFIGSRECO}" -l "${LOGGINGCONFIGS}"

# repeat experiment x2
# $PYTHON $RUN -c "${REPLAYCONFIGSRECO}" -l "${LOGGINGCONFIGS}"

cd ..
