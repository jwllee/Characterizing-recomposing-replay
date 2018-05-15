#!/usr/bin/env python

"""This is the example module.

This module does stuff.
"""


import os, sys
import numpy as np
import itertools as its

from opyenxes.data_in.XUniversalParser import XUniversalParser
from opyenxes.out.XesXmlGZIPSerializer import XesXmlGZIPSerializer
from opyenxes.classification.XEventNameClassifier import XEventNameClassifier
from opyenxes.factory.XFactory import XFactory
from opyenxes.model.XLog import XLog

__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


if __name__ == '__main__':
    datadir = os.path.join(
        '..', '..', 'data', 'synthetic', '2018-05-01_small'
    )

    nb_traces = 1000
    factory = XFactory()

    print(os.listdir(datadir))

    for dir in os.listdir(datadir):
        if not os.path.isdir(os.path.join(datadir, dir)):
            continue
        outdir = os.path.join(datadir, dir, 'l1000')
        os.makedirs(outdir)

        for xlog_filepath in os.listdir(os.path.join(datadir, dir, 'l5000')):
            if '.xes.gz' not in xlog_filepath:
                continue

            print('Processing {}'.format(xlog_filepath))

            with open(os.path.join(datadir, dir, xlog_filepath), 'r') as f:
                xlog = XUniversalParser().parse(f)[0]

            assert isinstance(xlog, XLog)

            new_xlog = factory.create_log(xlog.get_attributes())
            traces = np.random.choice(xlog, nb_traces, replace=False)
            new_xlog.get_classifiers().append(xlog.get_classifiers()[0])

            for t in traces:
                new_xlog.append(t)

            with open(outdir + os.sep + xlog_filepath, 'w') as f:
                XesXmlGZIPSerializer().serialize(new_xlog, f)
