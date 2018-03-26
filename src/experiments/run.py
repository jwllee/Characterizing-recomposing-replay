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


class Experiment:
    def __init__(self, configs):
        self.configs = configs
        self.basedir = self.configs['basedir']
        self.result_dir = self.configs['result_dir']
        self.outdir = self.configs['outdir']
        self.outfile = os.path.join(self.outdir, 'results.csv')
        self.init_outfile()
        self.datadir = os.path.join(self.basedir, self.configs['datadir'])

    def init_outfile(self):
        utils.writeheader(self.outfile, ReplayerConfiguration.HEADER)

    def make_prom_executor(self, configs_fpath, logfile):
        executor = ProMPluginExecutor(basedir=self.basedir,
                                      configs_fpath=configs_fpath,
                                      memory=self.configs['memory'],
                                      prom_jar=self.configs['prom_jar'],
                                      prom_pkg=self.configs['prom_pkg'],
                                      plugin_jar=self.configs['plugin_jar'],
                                      main_class=self.configs['main_class'],
                                      logfile=logfile)
        return executor

    def make_logfile(self, replay_id):
        filename = '{}.log'.format(replay_id)
        logfpath = os.path.join(self.outdir, filename)
        return logfpath

    def write_config_file(self, replay_id, configs):
        filename = 'replayConfigs{}.json'.format(replay_id)
        replay_config_fpath = os.path.join(self.outdir, filename)
        json_dict = configs.as_dict()
        with open(replay_config_fpath, 'w') as f:
            json.dump(json_dict, f)
        return replay_config_fpath

    def run(self):
        if self.configs['is_monolithic']:
            self.run_monolithic_replay()
        else:
            self.run_recomposition_replay()

    def run_monolithic_replay(self):
        logger.info('Running monolithic replay...')
        data_list = list()
        to_run_fpath = os.path.join(self.basedir, self.configs['data_to_run'])
        with open(to_run_fpath, 'r') as f:
            cnt = 0
            for line in f:
                model, log = line.split(',')
                model = model.strip()
                log = log.strip()
                logger.debug('Model {}: {}, Log {}: {}'.format(cnt, model,
                                                               cnt, log))
                data_list.append((model, log))
                cnt += 1

        for replay_id, to_run in enumerate(data_list):
            model = to_run[0]
            log = to_run[1]
            model_fpath = '.'.join([model, self.configs['model_ext']])
            log_fpath = '.'.join([log, self.configs['log_ext']])
            model_fpath = os.path.join(self.datadir, model, model_fpath)
            log_fpath = os.path.join(self.datadir, model, log_fpath)
            # create a configuration dict for MonolithicReplayer
            configs = MonolithicReplayerConfiguration(
                replay_config=self.configs['replay_config'],
                replay_id=replay_id,
                outfile=self.outfile,
                move_on_log_costs=self.configs['move_on_log_costs'],
                move_on_model_costs=self.configs['move_on_model_costs'],
                deadline=self.configs['deadline'],
                model=model,
                log=log,
                model_fpath=model_fpath,
                log_fpath=log_fpath
            )
            configs_fpath = self.write_config_file(replay_id, configs)
            logfile = self.make_logfile(replay_id)
            logfile = open(logfile, 'w')
            prom_executor = self.make_prom_executor(configs_fpath, logfile)
            # make replayer and replay
            replayer = MonolithicReplayer(configs=configs,
                                          outdir=self.outdir,
                                          prom_executor=prom_executor)
            replayer.replay()

    def run_recomposition_replay(self):
        logger.info('Running recomposition replay...')
        data_list = list()
        to_run_fpath = os.path.join(self.basedir, self.configs['data_to_run'])
        with open(to_run_fpath, 'r') as f:
            cnt = 0
            for line in f:
                model, log = line.split(',')
                model = model.strip()
                log = log.strip()
                logger.debug('Model {}: {}, Log {}: {}'.format(cnt, model,
                                                               cnt, log))
                data_list.append((model, log))
                cnt += 1

        for replay_id, to_run in enumerate(data_list):
            model = to_run[0]
            log = to_run[1]
            model_fpath = '.'.join([model, self.configs['model_ext']])
            log_fpath = '.'.join([log, self.configs['log_ext']])
            model_fpath = os.path.join(self.datadir, model, model_fpath)
            log_fpath = os.path.join(self.datadir, model, log_fpath)
            # make initial decomposition filepath
            init_decomp_file = model + '.' + self.configs['decomposition']
            init_decomp_file = os.path.join(self.datadir, model, 'decomposition', init_decomp_file)
            # create a configuration dict for RecompositionReplayer
            configs = RecompositionReplayerConfiguration(
                replay_config=self.configs['replay_config'],
                replay_id=replay_id, outfile=self.outfile,
                move_on_log_costs=self.configs['move_on_log_costs'],
                move_on_model_costs=self.configs['move_on_model_costs'],
                global_duration=self.configs['global_duration'],
                local_duration=self.configs['local_duration'],
                interval_relative=self.configs['interval_relative'],
                interval_absolute=self.configs['interval_absolute'],
                max_conflicts=self.configs['max_conflicts'],
                alignment_percentage=self.configs['alignment_percentage'],
                nb_of_iterations=self.configs['nb_of_iterations'],
                use_hide_n_reduce=self.configs['use_hide_n_reduce'],
                init_decomp_file=init_decomp_file,
                model=model, log=log, model_fpath=model_fpath, log_fpath=log_fpath
            )
            configs_fpath = self.write_config_file(replay_id, configs)
            logfile = self.make_logfile(replay_id)
            logfile = open(logfile, 'w')
            prom_executor = self.make_prom_executor(configs_fpath, logfile)
            # make replayer and replay
            replayer = RecompositionReplayer(configs=configs,
                                          outdir=self.outdir,
                                          prom_executor=prom_executor)
            replayer.replay()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', action='store',
                        dest='config_json',
                        help='Experiment configuration json file')
    parser.add_argument('-l', action='store',
                        dest='logging_json',
                        help='Python logger configuration json file path')

    args = parser.parse_args()

    with open(args.config_json, 'r') as f:
        configs = json.load(f)

    # get datetime
    dt = datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f')
    # make the out directory for this experiment
    basedir = configs['basedir']
    result_dir = os.path.join(basedir, configs['result_dir'])
    outdir = '_'.join([dt, configs['experiment_name']])
    outdir = os.path.join(result_dir, outdir)
    # need to make out directory
    os.makedirs(outdir)

    # update the outdir, resultdir
    configs['outdir'] = outdir
    configs['result_dir'] = result_dir

    utils.setup_logging(
        logdir=outdir,
        default_path=args.logging_json
    )
    logger.info('Finished setting up logger')

    experiment = Experiment(configs)
    experiment.run()
