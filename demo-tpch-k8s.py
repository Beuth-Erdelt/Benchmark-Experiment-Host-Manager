"""
    Demo for bexhoma
    This compares MonetDB and PostgreSQL performing some some TPC-H queries.
    The cluster is managed using Kubernetes.
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
import gc

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

# continue previous experiment?
code=None
# pick query file
queryfile = 'queries-tpch.config'
# pick scaling factor
SF = '1'
# number of repetition
numExperiments = 1
# pick hardware
cpu = "4000m"
memory = '16Gi'
cpu_type = 'epyc-7542'

# set basic config
cluster = masterK8s.testdesign(
	clusterconfig = 'cluster.config',
	yamlfolder = 'k8s/',
	configfolder = 'experiments/tpch',
	queryfile = queryfile)

# remove existing pods
cluster.cleanExperiment()

# set data volume
cluster.set_experiment(volume='tpch')

# set DDL scripts
cluster.set_experiment(script='1s-SF'+SF+'-index')

# continue previous experiment?
cluster.set_code(code=code)

# set workload parameters - this overwrites infos given in the query file
cluster.set_workload(
	name = 'TPC-H Queries',
	info = 'This experiment compares instances of different DBMS on different machines.'
	)

# set connection parameters - this overwrites infos given in the query file
cluster.set_connectionmanagement(
	numProcesses = 1,
	runsPerConnection = 0,
	timeout = 600)

# set query parameters - this overwrites infos given in the query file
cluster.set_querymanagement(numRun = 1)

# set hardware requests and limits
cluster.set_resources(
	requests = {
		'cpu': cpu,
		'memory': memory
	},
	limits = {
		'cpu': 0,
		'memory': 0
	},
	nodeSelector = {
		#'cpu': cpu_type,
	})


# function to capture recurring parts of the workflow
def run_experiments(docker, alias):
	cluster.set_experiment(docker=docker)
	cluster.set_experiment(instance=cpu+"-"+memory)
	cluster.prepareExperiment(delay=60)
	cluster.startExperiment(delay=60)
	for i in range(1,numExperiments+1):
		connection = cluster.getConnectionName()
		cluster.runBenchmarks(connection=connection+"-"+str(i), alias=alias+'-'+str(i))
	cluster.stopExperiment(delay=60)
	cluster.cleanExperiment(delay=60)
	del gc.garbage[:]


# run experiments
run_experiments(docker='MonetDB', alias='DBMS-A')
run_experiments(docker='PostgreSQL', alias='DBMS-B')

# run reporting
cluster.runReporting()

exit()

