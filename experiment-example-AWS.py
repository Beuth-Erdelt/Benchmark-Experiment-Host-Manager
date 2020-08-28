"""
    Small demo for running experiments in an AWS cluster. This deals with some TPC-H tests for bexhoma.
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
cluster = masterAWS.testdesign(
	clusterconfig='cluster.config',
	configfolder='experiments/example/')
# Do not resume an existing experiment
cluster.code=None
# Set benchmark settings - clients
cluster.connectionmanagement['numProcesses'] = 4
cluster.connectionmanagement['runsPerConnection'] = 0
cluster.connectionmanagement['timeout'] = 1200
# Remove old experiments
cluster.cleanExperiment()
# Set Experiment configuration
cluster.setExperiment(volume='tpch')
# TPC-H data in 1 shard, scaling factor = 1
cluster.setExperiment(script='small')


# Run benchmarks on AWS instance - 3 different DBMS
cluster.prepareExperiment(instance='64Gb')
cluster.startExperiment(docker='MemSQL')
cluster.runBenchmarks()
cluster.stopExperiment()
cluster.startExperiment(docker='PostgreSQL')
cluster.runBenchmarks()
cluster.stopExperiment()
cluster.startExperiment(docker='MariaDB')
cluster.runBenchmarks()
cluster.stopExperiment()
cluster.cleanExperiment()

# Run benchmarks on AWS instance - 1 DBMS, 4 different client settings
cluster.prepareExperiment(instance='512Gb')
cluster.startExperiment(docker='MemSQL')
cluster.connectionmanagement['numProcesses'] = 1
cluster.connectionmanagement['runsPerConnection'] = 1
connection = cluster.getConnectionName()
cluster.runBenchmarks(connection+"-1c-1l")
cluster.stopExperiment()
cluster.startExperiment()
cluster.connectionmanagement['numProcesses'] = 32
cluster.connectionmanagement['runsPerConnection'] = 1
connection = cluster.getConnectionName()
cluster.runBenchmarks(connection+"-32c-1l")
cluster.stopExperiment()
cluster.startExperiment()
cluster.connectionmanagement['numProcesses'] = 4
cluster.connectionmanagement['runsPerConnection'] = 8
connection = cluster.getConnectionName()
cluster.runBenchmarks(connection+"-4c-8l")
cluster.stopExperiment()
cluster.startExperiment()
cluster.connectionmanagement['numProcesses'] = 8
cluster.connectionmanagement['runsPerConnection'] = 4
connection = cluster.getConnectionName()
cluster.runBenchmarks(connection+"-8c-4l")
cluster.stopExperiment()
cluster.cleanExperiment()


# Run benchmarks of OmniSci - 1 DBMS, 2 different instances
cluster.setExperiment(docker='OmniSci')
cluster.runExperiment(instance='1xK80')
cluster.runExperiment(instance='1xV100')

exit()
