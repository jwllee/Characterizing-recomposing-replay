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


from src.experiments import utils
from src.experiments.executor import *
from src.preprocess.configuration import *


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


logger = logging.getLogger(__name__)


class DataCleaner:
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

    def clean(self):
        logger.info('Cleaning data...')
        data_list = list()
        to_clean_fpath = os.path.join(self.basedir, self.configs['data_to_clean'])
        with open(to_clean_fpath, 'r') as f:
            cnt = 0
            for line in f:
                model_dirname, model, log = line.split(',')
                model_dirname = model_dirname.strip()
                model = model.strip()
                log = log.strip()
                logger.debug('Model {}: {}, Log {}: {}'.format(cnt, model,
                                                               cnt, log))
                data_list.append((model_dirname, model, log))
                cnt += 1
        for model_dirname, model, log in data_list:
            log_fpath_dirty = '.'.join([log, self.configs['log_dirty_ext']])
            log_fpath_dirty = os.path.join(self.datadir, model_dirname, 'dirty', log_fpath_dirty)
            model_fpath_dirty = '.'.join([model, self.configs['model_dirty_ext']])
            model_fpath_dirty = os.path.join(self.datadir, model_dirname, 'dirty', model_fpath_dirty)

            log_fpath_clean = '.'.join([log, self.configs['log_clean_ext']])
            log_fpath_clean = os.path.join(self.datadir, model_dirname, log_fpath_clean)
            model_fpath_clean = '.'.join([model, self.configs['model_clean_ext']])
            model_fpath_clean = os.path.join(self.datadir, model_dirname, model_fpath_clean)

            configs = DataCleanConfiguration(
                log_fpath_dirty=log_fpath_dirty,
                model_fpath_dirty=model_fpath_dirty,
                log_fpath_clean=log_fpath_clean,
                model_fpath_clean=model_fpath_clean,
                classifier_type=self.configs['classifier_type']
            )

            directory = os.path.join(self.datadir, model_dirname, 'dirty')
            configs_fpath = self.write_config_file(model, directory, configs)
            logfile = self.make_logfile(model, directory)
            logfile = open(logfile, 'w')
            prom_executor = self.make_prom_executor(configs_fpath, logfile)
            logger.info('Cleaning {} (model) {} (log)...'.format(model, log))
            prom_executor.execute()





if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', action='store',
        dest='config_json',
        help='Data cleaner configuration json file'
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

    cleaner = DataCleaner(configs)
    cleaner.clean()
