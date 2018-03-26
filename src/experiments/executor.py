#!/usr/bin/env python

"""This is the example module.

This module does stuff.
"""

import os, logging, sys, subprocess


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"
__all__ = [ 'ProMPluginExecutor' ]


to_add = os.path.abspath(__file__)
to_add = to_add.split(os.sep)[:-3]
sys.path.append(os.sep.join(to_add))


logger = logging.getLogger(__name__)


class ProMPluginExecutor(object):

    def __init__(self, basedir, configs_fpath, memory, prom_jar,
                 prom_pkg, plugin_jar, main_class, logfile):
        self.basedir = basedir
        self.configs_fpath = configs_fpath
        self.memory = memory
        self.prom_jar = prom_jar
        self.prom_pkg = prom_pkg
        self.plugin_jar = plugin_jar
        self.main_class = main_class
        self.logfile = logfile

    def make_classpath(self):
        # add all libraries in lib
        # list directory of prom_pkg
        classpath = '.{pathsep}{prom_jar}{pathsep}' \
                    '{plugin_jar}'.format(pathsep=os.pathsep,
                                        prom_jar=self.prom_jar,
                                        plugin_jar=self.plugin_jar)

        for f in os.listdir(self.prom_pkg):
            if '.jar' in f:
                jar_filepath = os.path.join('.', self.prom_pkg, f)
                classpath += '{pathsep}{jar}'.format(pathsep=os.pathsep,
                                                     jar=jar_filepath)

        logger.debug('Classpath: {}'.format(classpath))

        return classpath

    def execute(self):
        logger.info('Executing...')
        classpath = self.make_classpath()
        command = 'java -classpath {classpath} ' \
                  '-Djava.library.path={prom_pkg} ' \
                  '-Djava.util.Arrays.useLegacyMergeSort=true ' \
                  '-Xmx{memory}G -XX:MaxPermSize=256m ' \
                  '{main_class} {configs_fpath}'.format(classpath=classpath,
                                                 prom_pkg=self.prom_pkg,
                                                 memory=self.memory,
                                                 main_class=self.main_class,
                                                 configs_fpath=self.configs_fpath)
        logger.info('Calling: {}'.format(command))
        logger.info('Current working directory: {}'.format(os.getcwd()))
        subprocess.call(command, shell=True, stdout=self.logfile)