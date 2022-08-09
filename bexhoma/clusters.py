"""
:Date: 2022-05-01
:Version: 0.5
:Authors: Patrick Erdelt

    Class to managing experiments in a cluster
    Copyright (C) 2020  Patrick Erdelt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import client, config
import subprocess
import os
import time
from timeit import default_timer
import psutil
import logging
import socket
import yaml
from tqdm import tqdm
from collections import Counter
import shutil
import json
import ast
import copy

from dbmsbenchmarker import *
from bexhoma import masterK8s, experiments


class kubernetes(masterK8s.testdesign):
    def __init__(self, clusterconfig='cluster.config', configfolder='experiments/', yamlfolder='k8s/', context=None, code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        # list of configurations (connections, docker)
        # per configuration: sut+service
        # per configuration: monitoring+service
        # per configuration: list of benchmarker
        self.code = code
        masterK8s.testdesign.__init__(self, clusterconfig=clusterconfig, configfolder=configfolder, context=context, yamlfolder=yamlfolder, code=self.code, instance=instance, volume=volume, docker=docker, script=script, queryfile=queryfile)
        self.max_sut = None
        self.experiments = []
    def add_experiment(self, experiment):
        self.experiments.append(experiment)
    def store_pod_log(self, pod_name, container=''):
        # write pod log
        stdout = self.pod_log(pod_name, container)
        filename_log = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/'+pod_name+'.log'
        f = open(filename_log, "w")
        f.write(stdout)
        f.close()




class aws(kubernetes):
    def __init__(self, clusterconfig='cluster.config', configfolder='experiments/', yamlfolder='k8s/', context=None, code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        self.code = code
        kubernetes.__init__(self, clusterconfig=clusterconfig, configfolder=configfolder, context=context, yamlfolder=yamlfolder, code=self.code, instance=instance, volume=volume, docker=docker, script=script, queryfile=queryfile)
        self.cluster = self.contextdata['cluster']
    def eksctl(self, command):
        #fullcommand = 'eksctl --context {context} {command}'.format(context=self.context, command=command)
        fullcommand = 'eksctl {command}'.format(command=command)
        self.logger.debug('aws.eksctl({})'.format(fullcommand))
        #print(fullcommand)
        return os.popen(fullcommand).read()# os.system(fullcommand)
    def scale_nodegroup(self, nodegroup, size):
        #fullcommand = "eksctl scale nodegroup --cluster=Test-2 --nodes=0 --nodes-min=0 --name=Kleine_Gruppe"
        command = "scale nodegroup --cluster={cluster} --nodes={size} --name={nodegroup}".format(cluster=self.cluster, size=size, nodegroup=nodegroup)
        return self.eksctl(command)



