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

from src.experiments.executor import *
from src.decompose.configuration import DecomposerConfiguration
from src.experiments import utils


logger = logging.getLogger(__name__)


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"
__all__ = [ 'Decomposer' ]


class Decomposer:
    def __init__(self, configs):
        self.configs = configs
        self.basedir = self.configs['basedir']
        self.datadir = os.path.join(self.basedir, self.configs['datadir'])

    def make_prom_executor(self, configs_fpath, logfile):
        executor = ProMPluginExecutor(
            basedir=self.configs['basedir'],
            configs_fpath=configs_fpath,
            memory=self.configs['memory'],
            prom_jar=self.configs['prom_jar'],
            prom_pkg=self.configs['prom_pkg'],
            plugin_jar=self.configs['plugin_jar'],
            main_class=self.configs['main_class'],
            logfile=logfile
        )
        return executor

    def write_config_file(self, name, directory, configs):
        filename = '{}.json'.format(name)
        configs_fpath = os.path.join(directory, filename)
        json_dict = configs.as_dict()
        with open(configs_fpath, 'w') as f:
            json.dump(json_dict, f)
        return configs_fpath

    def make_logfile(self, name, directory):
        filename = '{}.log'.format(name)
        logfpath = os.path.join(directory, filename)
        return logfpath

    def build_fname(self, decomposition_strategy,
                    percentage, max_subnet_arcs):
        if decomposition_strategy == 'Generic':
            fname = 'generic_{}'.format(percentage)
            return fname

        if decomposition_strategy == 'SESE-based':
            fname = 'sese_{}'.format(max_subnet_arcs)
            return fname

    def decompose(self):
        logger.info('Decomposing nets...')
        data_list = list()
        to_decompose_fpath = os.path.join(self.basedir, self.configs['data_to_decompose'])
        with open(to_decompose_fpath, 'r') as f:
            cnt = 0
            for line in f:
                model_dirname, model = line.split(',')
                model_dirname = model_dirname.strip()
                model = model.strip()
                logger.debug('Model {}: {}'.format(cnt, model))
                data_list.append((model_dirname, model))
                cnt += 1
        logger.info('There are {} nets to decompose.'.format(len(data_list)))

        for model_dirname, model in data_list:
            model_fpath = '.'.join([model, self.configs['model_ext']])
            model_fpath = os.path.join(self.datadir, model_dirname, model_fpath)

            max_subnet_arcs = self.configs['max_subnet_arcs'] if 'max_subnet_arcs' in self.configs else None
            percentage = self.configs['percentage'] if 'percentage' in self.configs else None

            fname = self.build_fname(self.configs['decomposition_strategy'],
                                     percentage, max_subnet_arcs)

            net_array_fpath = '{}.apna'.format(fname)
            net_array_fpath = os.path.join(self.datadir, model_dirname,
                                           'decomposition', fname, net_array_fpath)

            unsplittable_fpath = 'unsplittable.{}'.format(fname)
            unsplittable_fpath = os.path.join(self.datadir, model_dirname,
                                              'decomposition', fname, unsplittable_fpath)

            if not os.path.exists(unsplittable_fpath):
                # create an empty unsplittable file if it does not exists,
                # assuming that there are no unsplittable activities
                os.makedirs(os.path.join(self.datadir, model_dirname, 'decomposition', fname))
                with open(unsplittable_fpath, 'w') as f:
                    f.write('')

            # build configuration instance
            configs = DecomposerConfiguration(
                net_fpath=model_fpath,
                classifier_type=self.configs['classifier_type'],
                decomposition_strategy=self.configs['decomposition_strategy'],
                net_array_fpath=net_array_fpath,
                include_cluster_trans=self.configs['include_cluster_trans'],
                unsplittable_fpath=unsplittable_fpath,
                percentage=percentage,
                max_subnet_arcs=max_subnet_arcs
            )

            # write the JSON configuration and log file in the model
            # decomposition directory
            directory = os.path.join(self.datadir, model_dirname, 'decomposition', fname)
            configs_fpath = self.write_config_file(fname, directory, configs)
            logfile = self.make_logfile(model, directory)
            logfile = open(logfile, 'w')
            prom_executor = self.make_prom_executor(configs_fpath, logfile)
            logger.info('Decomposing model: {}'.format(model))
            prom_executor.execute()

        logger.info('Finished decomposition')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', action='store',
        dest='config_json',
        help='Net decomposer configuation json file'
    )

    parser.add_argument(
        '-l', action='store',
        dest='logging_json',
        help='Python logger configuration json file path'
    )

    args = parser.parse_args()

    with open(args.config_json, 'r') as f:
        configs = json.load(f)

    utils.setup_logging(default_path=args.logging_json)

    logger.info('Finished setting up logger')

    decomposer = Decomposer(configs)
    decomposer.decompose()
