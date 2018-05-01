#!/usr/bin/env python

"""This is the example module.

This module does stuff.
"""

__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"
__all__ = [ 'AcceptingPetriNetMetricsConfiguration' ]


class AcceptingPetriNetMetricsConfiguration:
    def __init__(self, model_fpath, outfile):
        self.model_fpath = model_fpath
        self.outfile = outfile

    def as_dict(self):
        json_dict = {
            'netPath': self.model_fpath,
            'outFile': self.outfile
        }
        return json_dict

