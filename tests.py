"""
    This script contains some code snippets for testing the detached mode in Kubernetes

    Copyright (C) 2021  Patrick Erdelt

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
from dbmsbenchmarker import *
import logging
import urllib3
import logging
import argparse
import time


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

cluster = clusters.kubernetes()

experiment = experiments.tpch(cluster=cluster, SF=1, timeout=180*1, numExperiments=1, detached=True, code=cluster.code)
experiment.set_queries_full()
experiment.set_workload(
    name = 'TPC-H Queries SF='+str(1),
    info = 'This experiment compares run time and resource consumption of TPC-H queries in different DBMS.'
)

experiment.set_querymanagement_quicktest(numRun=1)

experiment.set_resources(
    requests = {
        'cpu': "4",
        'memory': "64Gi",
        'gpu': 0
    },
    limits = {
        'cpu': 0,
        'memory': 0
    },
    nodeSelector = {
        'cpu': '',
        'gpu': ''
    })


config = configurations.default(experiment=experiment, docker='MonetDB', alias='DBMS A', numExperiments=1, clients=[1])
config = configurations.default(experiment=experiment, docker='MemSQL', alias='DBMS B', numExperiments=1, clients=[1])

"""
config = configurations.default(experiment=experiment, docker='MariaDB', alias='DBMS C', numExperiments=1, clients=[1])
config = configurations.default(experiment=experiment, docker='PostgreSQL', alias='DBMS D', numExperiments=1, clients=[1])
config = configurations.default(experiment=experiment, docker='MySQL', alias='DBMS E', numExperiments=1, clients=[1])
config = configurations.default(experiment=experiment, docker='OmniSci', alias='DBMS F', numExperiments=1, clients=[1])
config.set_resources(
    requests = {
        'cpu': "4",
        'memory': "64Gi",
        'gpu': 1
    },
    limits = {
        'cpu': 0,
        'memory': 0
    },
    nodeSelector = {
        'cpu': '',
        'gpu': 'a100'
    })

"""

experiment.start_sut()
experiment.start_loading()

#experiment.wait(20)
#experiment.load_data()

list_clients = [1,4]

experiment.benchmark_list(list_clients)

experiment.evaluate_results()

experiment.stop_benchmarker()

cluster.stop_sut()

cluster.stop_dashboard()
cluster.start_dashboard()

"""
app = cluster.appname
component = 'sut'
configuration = 'MonetDB'
cluster.getPorts(app, component, experiment.code, configuration)


app = cluster.appname
component = 'sut'
configuration = 'MemSQL'
ports = cluster.getPorts(app, component, experiment.code, configuration)

app = cluster.appname
component = 'sut'
configuration = 'MemSQL'
services = cluster.getServices(app, component, experiment.code, configuration)


service = services[0]

forward = ['kubectl', 'port-forward', 'service/'+service] #bexhoma-service']#, '9091', '9300']#, '9400']
#forward = ['kubectl', 'port-forward', 'pod/'+self.activepod]#, '9091', '9300']#, '9400']
forward.extend(ports)
#forward = ['kubectl', 'port-forward', 'service/service-dbmsbenchmarker', '9091', '9300']#, '9400']
#forward = ['kubectl', 'port-forward', 'service/service-dbmsbenchmarker', portstring]
#forward = ['kubectl', 'port-forward', 'deployment/'+self.deployments[0], portstring]
your_command = " ".join(forward)
print(your_command)

import subprocess

subprocess.Popen(forward, stdout=subprocess.PIPE)


config.checkDBMS('localhost', 9091)
"""


"""


# all jobs of configuration - benchmarker
app = cluster.appname
component = 'benchmarker'
configuration = ''
jobs = cluster.getJobs(app, component, experiment.code, configuration)

# status per job
for job in jobs:
    success = cluster.getJobStatus(job)
    print(job, success)
    cluster.deleteJob(job)

# all pods to these jobs
cluster.getJobPods(app, component, experiment.code, configuration)
pods = cluster.getJobPods(app, component, experiment.code, configuration)
jobs = cluster.getJobs(app, component, experiment.code, configuration)

for p in pods:
    status = cluster.getPodStatus(p)
    print(p,status)
    cluster.deletePod(p)


"""




#config.start_sut()
#cluster.startExperiment(delay=60)
#config.loadData()

"""
config.connectionmanagement
config.ddl_parameters
config.resources
experiment.configurations
cluster.experiments
config.code


# sut of experiment - deployment
app = cluster.appname
component = 'sut'
configuration = ''
cluster.getDeployments(app, component, experiment.code, configuration)

# sut of experiment - service
app = cluster.appname
component = 'sut'
configuration = ''
cluster.getServices(app, component, experiment.code, configuration)

# sut of experiment - pod
app = cluster.appname
component = 'sut'
configuration = ''
cluster.getPods(app, component, experiment.code, configuration)

# monitoring of experiment - pod
app = cluster.appname
component = 'monitoring'
configuration = ''
cluster.getPods(app, component, experiment.code, configuration)

# benchmarker of experiment - pod
app = cluster.appname
component = 'benchmarker'
configuration = ''
cluster.getPods(app, component, experiment.code, configuration)

# all pods of experiment
app = cluster.appname
component = ''
configuration = ''
cluster.getPods(app, component, experiment.code, configuration)

# all jobs of experiment
app = cluster.appname
component = ''
configuration = ''
cluster.getJobs(app, component, experiment.code, configuration)
# all pods to these jobs
cluster.getJobPods(app, component, experiment.code, configuration)
pods = cluster.getJobPods(app, component, experiment.code, configuration)

# all jobs of configuration - benchmarker
app = cluster.appname
component = 'benchmarker'
configuration = ''
cluster.getJobs(app, component, experiment.code, configuration)
# all pods to these jobs
cluster.getJobPods(app, component, experiment.code, configuration)
pods = cluster.getJobPods(app, component, experiment.code, configuration)

# status per pod
for p in pods:
    status = cluster.getPodStatus(p)
    print(p,status)
    #if status == 'Succeeded':
    if status != 'Running':
        cluster.deletePod(p)

for p in pods:
    status = cluster.getPodStatus(p)
    print(p,status)
    cluster.deletePod(p)

# success of job
app = cluster.appname
component = 'benchmarker'
configuration = ''
success = cluster.getJobStatus(app=app, component=component, experiment=experiment.code, configuration=configuration)

jobs = cluster.getJobs(app, component, experiment.code, configuration)

# status per job
for job in jobs:
    success = cluster.getJobStatus(job)
    print(job, success)
    if success:
        cluster.deleteJob(job)



# status per job
for job in jobs:
    success = cluster.getJobStatus(job)
    print(job, success)
    cluster.deleteJob(job)

"""

"""
# stop sut
app = cluster.appname
component = 'sut'
configuration = 'MemSQL'
cluster.stop_sut()
"""

"""
# prepare sut
app = cluster.appname
component = 'sut'
configuration = 'MemSQL'
config.start_sut(app=app, component=component, experiment=experiment.code, configuration=configuration)
#cluster.startExperiment(delay=60)
config.loadData()


# prepare sut
app = cluster.appname
component = 'sut'
configuration = 'MemSQL'
config.start_sut(app=app, component=component, experiment=experiment.code, configuration=configuration)
#cluster.startExperiment(delay=60)
config.loadData()
"""


# start benchmarker job
"""
app = cluster.appname
component = 'benchmarker'
configuration = 'MemSQL'
client = '1'
config.run_benchmarker_pod(connection=configuration+'-'+client, app=app, component=component, experiment=experiment.code, configuration=configuration, client=client)
client = '2'
config.run_benchmarker_pod(connection=configuration+'-'+client, app=app, component=component, experiment=experiment.code, configuration=configuration, client=client)
client = '3'
config.run_benchmarker_pod(connection=configuration+'-'+client, app=app, component=component, experiment=experiment.code, configuration=configuration, client=client)
client = '4'
config.run_benchmarker_pod(connection=configuration+'-'+client, app=app, component=component, experiment=experiment.code, configuration=configuration, client=client)
"""


# all MonetDB jobs of experiment
"""
app = cluster.appname
component = 'benchmarker'
configuration = 'MemSQL'
jobs = cluster.getJobs(app, component, experiment.code, configuration)
# all pods to these jobs
cluster.getJobPods(app, component, experiment.code, configuration)


experiment.evaluate_results()

cluster.stop_dashboard()
cluster.start_dashboard()
"""

# start and stop monitoring MySQL
#config.start_monitoring()
#config.stop_monitoring()
