#!/usr/bin/env python

"""This is the example module.

This module does stuff.
"""

__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"
__all__ = [ 'DataCleanConfiguration' ]

class DataCleanConfiguration:
    def __init__(self, log_fpath_dirty, model_fpath_dirty,
                 log_fpath_clean, model_fpath_clean, classifier_type):
        self.log_fpath_dirty = log_fpath_dirty
        self.model_fpath_dirty = model_fpath_dirty
        self.log_fpath_clean = log_fpath_clean
        self.model_fpath_clean = model_fpath_clean
        self.classifier_type = classifier_type

    def as_dict(self):
        json_dict = {
            'logDirtyPath': self.log_fpath_dirty,
            'netDirtyPath': self.model_fpath_dirty,
            'logCleanPath': self.log_fpath_clean,
            'netCleanPath': self.model_fpath_clean,
            'classifierType': self.classifier_type
        }
        return json_dict