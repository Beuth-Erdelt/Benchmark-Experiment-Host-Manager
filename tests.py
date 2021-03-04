



from bexhoma import *
from dbmsbenchmarker import *
#import experiments
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


config = clusters.configuration(experiment=experiment, docker='MonetDB', alias='DBMS A', numExperiments=1, clients=[1])
config = clusters.configuration(experiment=experiment, docker='MemSQL', alias='DBMS B', numExperiments=1, clients=[1])


experiment.start_sut()
experiment.wait(10)
experiment.load_data()

list_clients = [4,8,16]

for i, parallelism in enumerate(list_clients):
    client = str(i+1)
    for config in experiment.configurations:
        config.run_benchmarker_pod(connection=config.docker+'-'+client, configuration=config.docker, client=client, parallelism=parallelism)
    while True:
        time.sleep(10)
        # all jobs of configuration - benchmarker
        app = cluster.appname
        component = 'benchmarker'
        configuration = ''
        jobs = cluster.getJobs(app, component, experiment.code, configuration)
        # all pods to these jobs
        pods = cluster.getJobPods(app, component, experiment.code, configuration)
        # status per pod
        for p in pods:
            status = cluster.getPodStatus(p)
            print(p,status)
            if status == 'Succeeded':
                #if status != 'Running':
                cluster.store_pod_log(p)
                cluster.deletePod(p)
            if status == 'Failed':
                #if status != 'Running':
                cluster.store_pod_log(p)
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
        if len(pods) == 0 and len(jobs) == 0:
            break

experiment.evaluate_results()

cluster.stop_sut()


cluster.stop_dashboard()
cluster.start_dashboard()




# all jobs of configuration - benchmarker
app = cluster.appname
component = 'benchmarker'
configuration = ''
cluster.getJobs(app, component, experiment.code, configuration)
# all pods to these jobs
cluster.getJobPods(app, component, experiment.code, configuration)
pods = cluster.getJobPods(app, component, experiment.code, configuration)
jobs = cluster.getJobs(app, component, experiment.code, configuration)

for p in pods:
    status = cluster.getPodStatus(p)
    print(p,status)
    cluster.deletePod(p)

jobs = cluster.getJobs(app, component, experiment.code, configuration)

# status per job
for job in jobs:
    success = cluster.getJobStatus(job)
    print(job, success)
    cluster.deleteJob(job)






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
