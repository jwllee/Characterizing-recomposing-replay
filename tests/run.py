#!/usr/bin/env python

"""This is the example module.

This module does stuff.
"""


import pytest, os, json, sys

import replay
import replayer

sys.path.append('../src')

from experiments import run


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


@pytest.fixture(scope='module')
def empty_replayer_config():
    return replayer.ReplayerConfig(0, 0)


@pytest.fixture(scope='module')
def empty_monolithic_replayer_config():
    return replayer.MonolithicReplayerConfig(0, 0, 0)


@pytest.fixture(scope='module')
def default_replayer_config():
    move_on_log_costs = 10
    move_on_model_costs = 4
    return replayer.ReplayerConfig(move_on_log_costs, move_on_model_costs)


@pytest.fixture(scope='module')
def default_monolithic_replayer_config(default_replayer_config):
    move_on_log_costs = default_replayer_config.move_on_log_costs
    move_on_model_costs = default_replayer_config.move_on_model_costs
    deadline = 100
    configuration = 'Do not decompose'
    return replayer.MonolithicReplayerConfig(deadline=deadline,
                                             configuration=configuration,
                                             move_on_log_costs=move_on_log_costs,
                                             move_on_model_costs=move_on_model_costs)


@pytest.fixture(scope='module')
def default_recomposing_replayer_config(default_replayer_config):
    global_duration = 100
    local_duration = 10
    interval_relative = 5
    interval_absolute = 5
    max_conflicts = 7
    alignment_perc = 80
    nb_of_iterations = 1000
    move_on_log_costs = default_replayer_config.move_on_log_costs
    move_on_model_costs = default_replayer_config.move_on_model_costs

    return replayer.RecomposingReplayerConfig(global_duration=global_duration,
                                              local_duration=local_duration,
                                              interval_relative=interval_relative,
                                              interval_absolute=interval_absolute,
                                              max_conflicts=max_conflicts,
                                              alignment_percentage=alignment_perc,
                                              max_iterations=nb_of_iterations,
                                              move_on_log_costs=move_on_log_costs,
                                              move_on_model_costs=move_on_model_costs)


@pytest.fixture(scope='module')
def default_replay_param(default_replayer_config):
    replay_id = 0
    model_name = 'default_model'
    model_dirty_path = 'model_dirty_path'
    log_dirty_path = 'log_dirty_path'
    model_clean_path = 'model_clean_path'
    log_clean_path = 'log_clean_path'
    clf_type = 'standard'
    replayer_config = default_replayer_config
    logfile = '0.log'
    outdir = 'out'
    outfile = '0.out'
    memory = 16
    prom_jar = 'prom_jar'
    prom_pkg = 'prom_pkg'
    boot_jar = 'boot_jar'
    return replay.ReplayParam(replay_id=replay_id,
                              model_name=model_name,
                              model_dirty_path=model_dirty_path,
                              log_dirty_path=log_dirty_path,
                              model_clean_path=model_clean_path,
                              log_clean_path=log_clean_path,
                              clf_type=clf_type, replayer_config=replayer_config,
                              logfile=logfile, outdir=outdir, outfile=outfile,
                              memory=memory, prom_jar=prom_jar, prom_pkg=prom_pkg,
                              boot_jar=boot_jar)


@pytest.fixture(scope='module')
def data_tmpdir(tmpdir_factory):
    return tmpdir_factory.mktemp('data')


@pytest.fixture(scope='module')
def monolithic_replayer_config_json(data_tmpdir, default_monolithic_replayer_config):
    file = data_tmpdir + os.sep + 'monolithic_replayer_config.json'
    with open(file, 'w') as f:
        json.dump(default_monolithic_replayer_config, f,
                  default=replayer.MonolithicReplayerConfig.to_json)
    return file


@pytest.fixture(scope='module')
def recomposing_replayer_config_json(data_tmpdir, default_recomposing_replayer_config):
    file = data_tmpdir + os.sep + 'recomposing_replayer_config.json'
    with open(file, 'w') as f:
        json.dump(default_recomposing_replayer_config, f,
                  default=replayer.RecomposingReplayerConfig.to_json)
    return file

class TestReplayerConfig:

    def test_repr(self, default_replayer_config):
        expected = 'ReplayerConfig(10, 4)'
        assert repr(default_replayer_config) == expected


class TestMonolithicReplayerConfig:

    def test_repr(self, default_monolithic_replayer_config):
        expected = 'MonolithicReplayerConfig(10, 4, Do not decompose, 100)'
        assert repr(default_monolithic_replayer_config) == expected

    @staticmethod
    def assert_config_equivalence(c1, c2):
        return c1.deadline == c2.deadline and \
               c1.configuration == c2.configuration and \
               c1.move_on_log_costs == c2.move_on_log_costs and \
               c1.move_on_model_costs == c2.move_on_model_costs

    def test_from_json(self, monolithic_replayer_config_json,
                       default_monolithic_replayer_config):
        config = replayer.MonolithicReplayerConfig.from_json(monolithic_replayer_config_json)
        assert TestMonolithicReplayerConfig.assert_config_equivalence(
            default_monolithic_replayer_config, config)


class TestRecomposingReplayerConfig:

    def test_repr(self, default_recomposing_replayer_config):
        expected = 'RecomposingReplayerConfig(10, 4, 100, 10, 5, 5, 7, 80, 1000)'
        assert repr(default_recomposing_replayer_config) == expected

    @staticmethod
    def assert_config_equivalence(c1, c2):
        return c1.move_on_log_costs == c2.move_on_log_costs and \
               c1.move_on_model_costs == c2.move_on_model_costs and \
               c1.global_duration == c2.global_duration and \
               c1.local_duration == c2.local_duration and \
               c1.interval_relative == c2.interval_relative and \
               c1.interval_absolute == c2.interval_absolute and \
               c1.max_conflicts == c2.max_conflicts and \
               c1.alignment_perc == c2.alignment_perc and \
               c1.nb_of_iterations == c2.nb_of_iterations

    def test_from_json(self, recomposing_replayer_config_json,
                       default_recomposing_replayer_config):
        config = replayer.RecomposingReplayerConfig.from_json(recomposing_replayer_config_json)
        assert TestRecomposingReplayerConfig.assert_config_equivalence(
            default_recomposing_replayer_config, config
        )


class TestReplayParam:

    def test_repr(self, default_replay_param, default_replayer_config):
        expected = 'ReplayParam(0, default_model, model_dirty_path, ' \
                   'log_dirty_path, model_clean_path, log_clean_path, ' \
                   'standard, {}, 0.log, out, 0.out, 16, ' \
                   'prom_jar, prom_pkg, boot_jar)'.format(repr(default_replayer_config))

        assert repr(default_replay_param) == expected

