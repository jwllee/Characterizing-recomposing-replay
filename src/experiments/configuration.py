#!/usr/bin/env python

"""This is the example module.

This module does stuff.
"""

import os, json, sys, logging


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"
__all__ = [ 'MonolithicReplayerConfiguration', 'RecompositionReplayerConfiguration',
            'ReplayerConfiguration']

to_add = os.path.abspath(__file__)
to_add = to_add.split(os.sep)[:-3]
sys.path.append(os.sep.join(to_add))


logger = logging.getLogger(__name__)


class ReplayerConfiguration(object):
    HEADER = ['_id', 'LogPath', "ModelPath", 'Log', 'Model', 'Monolithic',
              'Decomposition', 'GlobalDurationThreshold', 'LocalDurationThreshold',
              'LogMoveCost', 'ModelMoveCost',
              'RelativeIntervalThreshold', 'AbsoluteIntervalThreshold',
              'MaxConflictThreshold', 'AlignmentPercentageThreshold',
              'MaxIterationThreshold', 'CostIntervalLo', 'CostIntervalHi',
              'FitnessLo', 'FitnessHi', 'IsReliable', 'TotalTraces',
              'RecompositionStepsTaken', 'TotalTimeTaken']


class MonolithicReplayerConfiguration(ReplayerConfiguration):
    def __init__(self, replay_config, replay_id, outfile,
                 move_on_log_costs, move_on_model_costs, deadline,
                 model, log,
                 model_fpath, log_fpath):
        self.replay_config = replay_config
        self.replay_id = replay_id
        self.outfile = outfile
        self.move_on_log_costs = move_on_log_costs
        self.move_on_model_costs = move_on_model_costs
        self.deadline = deadline
        self.model = model
        self.log = log
        self.model_fpath = model_fpath
        self.log_fpath = log_fpath

    def as_dict(self):
        json_dict = { 'configuration': self.replay_config,
                      'iteration': self.replay_id,
                      'outFile': self.outfile,
                      'moveOnLogCosts': self.move_on_log_costs,
                      'moveOnModelCosts': self.move_on_model_costs,
                      'deadline': self.deadline,
                      'model': self.model,
                      'log': self.log,
                      'modelPath': self.model_fpath,
                      'logPath': self.log_fpath }
        return json_dict


class RecompositionReplayerConfiguration(ReplayerConfiguration):
    def __init__(self, replay_config, replay_id, outfile,
                 move_on_log_costs, move_on_model_costs,
                 global_duration, local_duration,
                 interval_relative, interval_absolute,
                 max_conflicts, alignment_percentage,
                 nb_of_iterations, use_hide_n_reduce, decomposition,
                 init_decomp_file, model, log, model_fpath, log_fpath):
        self.replay_config = replay_config
        self.replay_id = replay_id
        self.outfile = outfile
        self.move_on_log_costs = move_on_log_costs
        self.move_on_model_costs = move_on_model_costs
        self.global_duration = global_duration
        self.local_duration = local_duration
        self.interval_relative = interval_relative
        self.interval_absolute = interval_absolute
        self.max_conflicts = max_conflicts
        self.alignment_percentage = alignment_percentage
        self.nb_of_iterations = nb_of_iterations
        self.use_hide_n_reduce = use_hide_n_reduce
        self.decomposition = decomposition
        self.init_decomp_file = init_decomp_file
        self.model = model
        self.log = log
        self.model_fpath = model_fpath
        self.log_fpath = log_fpath

    def as_dict(self):
        json_dict = { 'iteration': self.replay_id,
                      'outFile': self.outfile,
                      'moveOnLogCosts': self.move_on_log_costs,
                      'moveOnModelCosts': self.move_on_model_costs,
                      'globalDuration': self.global_duration,
                      'localDuration': self.local_duration,
                      'intervalRelative': self.interval_relative,
                      'intervalAbsolute': self.interval_absolute,
                      'maxConflicts': self.max_conflicts,
                      'alignmentPercentage': self.alignment_percentage,
                      'nofIterations': self.nb_of_iterations,
                      'useHideAndReduceAbstraction': self.use_hide_n_reduce,
                      'decomposition': self.decomposition,
                      'initDecompFile': self.init_decomp_file,
                      'model': self.model,
                      'log': self.log,
                      'modelPath': self.model_fpath,
                      'logPath': self.log_fpath }
        return json_dict
