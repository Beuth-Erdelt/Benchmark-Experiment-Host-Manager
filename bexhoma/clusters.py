"""
    Class to managing experiments in a Kubernetes cluster
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
from timeit import default_timer #as timer
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
    def __init__(self, clusterconfig='cluster.config', configfolder='experiments/', yamlfolder='k8s/', code=None, instance=None, volume=None, docker=None, script=None, queryfile=None):
        # list of configurations (connections, docker)
        # per configuration: sut+service
        # per configuration: monitoring+service
        # per configuration: list of benchmarker
        self.code = code
        masterK8s.testdesign.__init__(self, clusterconfig=clusterconfig, configfolder=configfolder, yamlfolder=yamlfolder, code=self.code, instance=instance, volume=volume, docker=docker, script=script, queryfile=queryfile)
        self.max_sut = None
        """
        self.code = code
        if self.code is None:
            self.code = str(round(time.time()))
        self.path = self.resultfolder+"/"+self.code
        if not path.isdir(self.path):
            makedirs(self.path)
        """
        self.experiments = []
    def add_experiment(self, experiment):
        self.experiments.append(experiment)
    def store_pod_log(self, pod_name):
        # write pod log
        stdin, stdout, stderr = self.pod_log(pod_name)
        filename_log = self.config['benchmarker']['resultfolder'].replace("\\", "/").replace("C:", "")+"/"+str(self.code)+'/'+pod_name+'.log'
        f = open(filename_log, "w")
        f.write(stdout)
        f.close()



