"""
    Small demo for running experiments in an k8s cluster. This deals with some TPC-H tests for bexhoma.
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
from bexhoma import *
import logging
import urllib3

# Set logging
urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

# Set basic config folders
cluster = masterK8s.testdesign(
	clusterconfig='cluster.config',
	configfolder='experiments/example/',
	yamlfolder='k8s/')
# Do not resume an existing experiment
cluster.code=None
# Set benchmark settings - clients
cluster.connectionmanagement['numProcesses'] = 4
cluster.connectionmanagement['runsPerConnection'] = 0
cluster.connectionmanagement['timeout'] = 1200
# Remove old experiments
cluster.cleanExperiment()
# Set Experiment configuration
cluster.setExperiment(volume='example')
# TPC-H data in 1 shard, scaling factor = 1
cluster.setExperiment(script='small')

# Run benchmarks of OmniSci - in 4 different host settings
cluster.setExperiment(docker='OmniSci')
cluster.runExperiment(instance="4000m-64Gi-1-k80")
cluster.runExperiment(instance="8000m-64Gi-1-p100")
cluster.runExperiment(instance="16000m-128Gi-1-p100")
cluster.runExperiment(instance="16000m-128Gi-1-v100")

# Run benchmarks of MemSQL - in 2 different host settings
cluster.setExperiment(docker='MemSQL')
cluster.runExperiment(instance="8000m-64Gi")
cluster.runExperiment(instance="16000m-128Gi")

# Run benchmarks of PostgreSQL - in 1 host setting
cluster.setExperiment(docker='PostgreSQL')
cluster.runExperiment(instance="8000m-64Gi")

# Run benchmarks of MariDB - in 1 different host setting
cluster.setExperiment(docker='MariaDB')
cluster.runExperiment(instance="8000m-64Gi")


exit()
