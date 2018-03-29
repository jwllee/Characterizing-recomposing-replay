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
from src.decompose.configuration import SharedActivityFinderConfiguration
from src.experiments import utils


logger = logging.getLogger(__name__)


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"
__all__ = [ 'SharedActivityFinder' ]


class SharedActivityFinder:
    def __init__(self, configs):
        self.configs = configs
        self.basedir = self.configs['basedir']
        self.datadir = os.path.join(self.basedir, self.configs['datadir'])

    def make_prom_executor(self, confis_fpath, logfile):
        executor = ProMPluginExecutor(
            basedir=self.configs['basedir'],
            configs_fpath=confis_fpath,
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

    def find(self):
        logger.info('Finding shared activities...')
        data_list = list()
        to_run_fpath = os.path.join(self.basedir, self.configs['data_to_run'])
        with open(to_run_fpath, 'r') as f:
            cnt = 0
            for line in f:
                model_dirname, net_array_dirname, net_array = line.split(',')
                model_dirname = model_dirname.strip()
                net_array_dirname = net_array_dirname.strip()
                net_array = net_array.strip()
                logger.debug('Net array {}: {}'.format(cnt, net_array))
                data_list.append((model_dirname, net_array_dirname, net_array))
                cnt += 1
        logger.info('There are {} net arrays to find shared activities'.format(len(data_list)))

        for model_dirname, net_array_dirname, net_array in data_list:
            net_array_fpath = '.'.join([net_array, self.configs['net_array_ext']])
            net_array_fpath = os.path.join(self.datadir, model_dirname, 'decomposition',
                                           net_array_dirname, net_array_fpath)

            shared_acts_fpath = '{}.{}'.format(model_dirname, net_array)
            shared_acts_fpath = os.path.join(self.datadir, model_dirname,
                                             'decomposition', shared_acts_fpath)

            # build configuration instance
            configs = SharedActivityFinderConfiguration(
                net_array_fpath=net_array_fpath,
                shared_acts_fpath=shared_acts_fpath
            )

            # write the JSON configuration and log file in the net array
            # directory
            fname = 'shared-activities'
            directory = os.path.join(self.datadir, model_dirname,
                                     'decomposition', net_array_dirname)
            configs_fpath = self.write_config_file(fname, directory, configs)
            logfile = self.make_logfile(net_array, directory)
            logfile = open(logfile, 'w')
            prom_executor = self.make_prom_executor(configs_fpath, logfile)
            logger.info('Finding shared activities of net array: {}'.format(net_array))
            prom_executor.execute()

        logger.info('Finished finding shared activities.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', action='store',
        dest='config_json',
        help='Shared activities finder json file'
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

    finder = SharedActivityFinder(configs)
    finder.find()
