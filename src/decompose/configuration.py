#!/usr/bin/env python

"""This is the example module.

This module does stuff.
"""

import os, sys, logging, json
import argparse
from datetime import datetime

to_add = os.path.abspath(__file__)
to_add = to_add.split(os.sep)[:-3]
sys.path.append(os.sep.join(to_add))

# print('System paths: {}'.format(sys.path))

from src.experiments.replayer import *
from src.experiments.configuration import *
from src.experiments.executor import *
from src.experiments import utils


logger = logging.getLogger(__name__)


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"

__all__ = [ 'DecomposerConfiguration', 'SharedActivityFinderConfiguration' ]


class DecomposerConfiguration:
    def __init__(self, net_fpath, classifier_type, decomposition_strategy,
                 net_array_fpath, include_cluster_trans,
                 unsplittable_fpath, percentage, max_subnet_arcs):
        self.net_fpath = net_fpath
        self.classifier_type = classifier_type
        self.decomposition_strategy = decomposition_strategy
        self.net_array_fpath = net_array_fpath
        self.include_cluster_trans = include_cluster_trans
        self.unsplittable_fpath = unsplittable_fpath
        self.percentage = percentage
        self.max_subnet_arcs = max_subnet_arcs

    def as_dict(self):
        _dict = { 'netFilePath': self.net_fpath,
                  'classifierType': self.classifier_type,
                  'decompositionStrategy': self.decomposition_strategy,
                  'netArrayFilePath': self.net_array_fpath,
                  'includeClusterTransitions': self.include_cluster_trans,
                  'unsplittableFilePath': self.unsplittable_fpath,
                  'percentage': self.percentage,
                  'maxSubnetArcs': self.max_subnet_arcs
                }
        # need to remove some of the optional configs depending on the strategy
        if self.decomposition_strategy == 'SESE-based':
            del _dict['percentage']
        if self.decomposition_strategy == 'Generic':
            del _dict['maxSubnetArcs']

        return _dict


class SharedActivityFinderConfiguration:
    def __init__(self, net_array_fpath, shared_acts_fpath):
        self.net_array_fpath = net_array_fpath
        self.shared_acts_fpath = shared_acts_fpath

    def as_dict(self):
        _dict = { 'netArrayFilePath': self.net_array_fpath,
                  'sharedActsFilePath': self.shared_acts_fpath
                }
        return _dict
