#!/usr/bin/env python

"""This is the example module.

This module does stuff.
"""


import sys, os, logging, json
import argparse


to_add = os.path.abspath(__file__)
to_add = to_add.split(os.sep)[:-3]
sys.path.append(os.sep.join(to_add))


from src.experiments import utils
from src.experiments.executor import *
from src.metrics.configuration import *


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


logger = logging.getLogger(__name__)


class MetricCalculator:
    def __init__(self, configs):
        self.configs = configs
        self.basedir = self.configs['basedir']
        self.datadir = os.path.join(self.basedir, self.configs['datadir'])

    def write_config_file(self, name, directory, configs):
        filename = '{}.json'.format(name)
        configs_fpath = os.path.join(directory, filename)
        json_dict = configs.as_dict()
        with open(configs_fpath, 'w') as f:
            json.dump(json_dict, f)
        return configs_fpath

    def make_prom_executor(self, configs_fpath):
        executor = ProMPluginExecutor(
            basedir=self.configs['basedir'],
            configs_fpath=configs_fpath,
            memory=self.configs['memory'],
            prom_jar=self.configs['prom_jar'],
            prom_pkg=self.configs['prom_pkg'],
            plugin_jar=self.configs['plugin_jar'],
            main_class=self.configs['main_class'],
        )
        return executor

    def compute(self):
        logger.info('Computing metrics for accepting petri net...')
        data_list = list()
        to_compute_fpath = os.path.join(self.basedir, self.configs['data_to_compute'])
        with open(to_compute_fpath, 'r') as f:
            cnt = 0
            for line in f:
                model_dirname, model = line.split(',')
                model_dirname = model_dirname.strip()
                model = model.strip()
                logger.debug('Model {}: {}'.format(cnt, model))
                data_list.append((model_dirname, model))
                cnt += 1

        for model_dirname, model in data_list:
            model_fpath = '.'.join([model, self.configs['model_ext']])
            model_fpath = os.path.join(self.datadir, model_dirname, model_fpath)
            metrics_csv = os.path.join(self.datadir, model_dirname, 'metrics.csv')

            configs = AcceptingPetriNetMetricsConfiguration(
                model_fpath=model_fpath, outfile=metrics_csv)

            directory = os.path.join(self.datadir, model_dirname)
            configs_fpath = self.write_config_file(model, directory, configs)

            prom_executor = self.make_prom_executor(configs_fpath)
            logger.info('Computing metrics for {}'.format(model))
            prom_executor.execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', action='store',
        dest='config_json',
        help='Petri net metric computer json file'
    )

    parser.add_argument(
        '-l', action='store',
        dest='logging_json',
        help='Python logger configuration json file path'
    )

    args = parser.parse_args()

    with open(args.config_json, 'r') as f:
        configs = json.load(f)

    utils.setup_logging(
        default_path=args.logging_json
    )
    logger.info('Finished setting up logger')

    computer = MetricCalculator(configs)
    computer.compute()
