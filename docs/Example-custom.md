# Example: Run a custom SQL workload

This example assumes you have
* a DBMS installed outside of bexhoma
* a database loaded
* a sequence of SQL queries you want to run against the database

## Prerequisites

We need a dummy to mimick the existence of a DBMS managed by bexhoma and a query file in a certain format.

### Dummy DBMS

Inside the `docker` section of the `cluster.config` we define infos how to connect to a DBMS (keep key `Dummy` here, adjust all the rest):
```
        'Dummy': {
            'loadData': '',
            'delay_prepare': 0,
            'template': {
                'version': 'v1.0',
                'alias': 'Dummy',
                'docker_alias': 'ABC',
                 'JDBC': {
                    'driver': "com.yugabyte.Driver",
                    'auth': ["yugabyte", ""],
                    'url': 'jdbc:yugabytedb://yb-tserver-service.perdelt.svc.cluster.local:5433/yugabyte?load-balance=true',
                    'jar': 'jdbc-yugabytedb-42.3.5-yb-2.jar'
                }
            },
            'logfile': '/usr/local/data/logfile',
            'datadir': '/var/lib/postgresql/data/',
            'priceperhourdollar': 0.0,
        },
```

### Queries File

Overwrite the file `queries.config` in `experiments/example` with a custom file.
For more details about the format see https://dbmsbenchmarker.readthedocs.io/en/latest/Options.html#query-file


## Run Experiment

Example: Run `python example.py run -dbms Dummy -ne 5 -nr 100` to run experiment with 5 parallel benchmarkers and repeat each query 100 times.

## Background Information

1. The script installs a Dummy DBMS according to `k8s/deploymenttemplate-Dummy.yml`. This is just a lightweight busybox container running an endless sleep. Bexhoma writes status information about the components to the benchmarked DBMS container. If the DBMS is not managed by bexhoma, we need such a Dummy container otherwise. The container will be removed automatically after experiment has finished.

The DBMSBenchmarker Docker container needs to have the required JDBC driver included.

Currently, the image contains the following:
```

######### Specific version of PostgreSQL JDBC #########
RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.0.jar --no-check-certificate
RUN cp postgresql-42.5.0.jar jars/postgresql-42.5.0.jar

######### Specific version of MySQL JDBC #########
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-8.0.31.tar.gz
RUN tar -zxvf mysql-connector-j-8.0.31.tar.gz
RUN cp mysql-connector-j-8.0.31/mysql-connector-j-8.0.31.jar jars/mysql-connector-j-8.0.31.jar

######### Specific version of MariaDB JDBC #########
RUN wget https://dlm.mariadb.com/2678616/Connectors/java/connector-java-3.1.0/mariadb-java-client-3.1.0.jar
RUN cp mariadb-java-client-3.1.0.jar jars/mariadb-java-client-3.1.0.jar

######### Specific version of MonetDB JDBC #########
RUN wget https://www.monetdb.org/downloads/Java/archive/monetdb-jdbc-3.3.jre8.jar --no-check-certificate
RUN cp monetdb-jdbc-3.3.jre8.jar jars/monetdb-jdbc-3.3.jre8.jar

######### Specific version of MonetDB JDBC #########
RUN wget https://www.monetdb.org/downloads/Java/monetdb-jdbc-3.3.jre8.jar --no-check-certificate
RUN cp monetdb-jdbc-3.3.jre8.jar jars/monetdb-jdbc-3.3.jre8.jar

######### Specific version of SingleStore JDBC #########
RUN wget https://github.com/memsql/S2-JDBC-Connector/releases/download/v1.1.4/singlestore-jdbc-client-1.1.4.jar
RUN cp singlestore-jdbc-client-1.1.4.jar jars/singlestore-jdbc-client-1.1.4.jar

######### Specific version of Kinetica JDBC #########
RUN wget https://github.com/kineticadb/kinetica-client-jdbc/archive/refs/tags/v7.1.8.7.tar.gz
RUN tar -zxvf v7.1.8.7.tar.gz
RUN cp kinetica-client-jdbc-7.1.8.7/kinetica-jdbc-7.1.8.7-jar-with-dependencies.jar jars/kinetica-jdbc-7.1.8.7-jar-with-dependencies.jar

######### Specific version of YugabyteDB JDBC #########
RUN wget https://github.com/yugabyte/pgjdbc/releases/download/v42.3.5-yb-2/jdbc-yugabytedb-42.3.5-yb-2.jar
RUN cp jdbc-yugabytedb-42.3.5-yb-2.jar jars/jdbc-yugabytedb-42.3.5-yb-2.jar
```

## Status and Evaluation

You can see the status of running experiments via `bexperiments status`

Finished experiments can be inspected locally or using the dashboard container.
`bexperiments dashboard` forwards to dashboard to `localhost:8888`.
You can connect to a Jupyter server there (password is admin).

There is a variety of evaluation tools included.
For example to compute the total throughput:
```
from dbmsbenchmarker import *

resultfolder = "/results/"
code = "1234"

# load merged results
evaluate = inspector.inspector(resultfolder)
evaluate.load_experiment(code)

# read dict of benchmarking times per stream
list_connections = evaluate.get_experiment_list_connections()
benchmarker_times = evaluate.get_experiment_connection_properties(list_connections[0])['times']['total']

# compute min of start and max of end for timespan
times_start=[]
times_end=[]
for t in benchmarker_times:
    times_start.append(benchmarker_times[t]['time_start'])
    times_end.append(benchmarker_times[t]['time_end'])

time_start = min(times_start)
time_end = max(times_end)
print(time_start, time_end, time_end-time_start)
```
might print something like `1691160697 1691160833 136` (total time of 136 seconds).

The dict `benchmarker_times` contains (for 20 parallel benchmarkers) something like
```
Dummy-BHT-1-1-1-9
  time_start:1691160740
  time_end:1691160741
Dummy-BHT-1-1-1-19
  time_start:1691160825
  time_end:1691160826
Dummy-BHT-1-1-1-6
  time_start:1691160717
  time_end:1691160719
Dummy-BHT-1-1-1-20
  time_start:1691160831
  time_end:1691160833
Dummy-BHT-1-1-1-5
  time_start:1691160716
  time_end:1691160718
Dummy-BHT-1-1-1-12
  time_start:1691160759
  time_end:1691160761
Dummy-BHT-1-1-1-17
  time_start:1691160802
  time_end:1691160804
Dummy-BHT-1-1-1-10
  time_start:1691160742
  time_end:1691160744
Dummy-BHT-1-1-1-3
  time_start:1691160703
  time_end:1691160705
Dummy-BHT-1-1-1-8
  time_start:1691160730
  time_end:1691160732
Dummy-BHT-1-1-1-11
  time_start:1691160751
  time_end:1691160753
Dummy-BHT-1-1-1-15
  time_start:1691160782
  time_end:1691160784
Dummy-BHT-1-1-1-4
  time_start:1691160709
  time_end:1691160711
Dummy-BHT-1-1-1-7
  time_start:1691160727
  time_end:1691160728
Dummy-BHT-1-1-1-2
  time_start:1691160699
  time_end:1691160700
Dummy-BHT-1-1-1-16
  time_start:1691160791
  time_end:1691160792
Dummy-BHT-1-1-1-13
  time_start:1691160767
  time_end:1691160769
Dummy-BHT-1-1-1-1
  time_start:1691160697
  time_end:1691160698
Dummy-BHT-1-1-1-14
  time_start:1691160778
  time_end:1691160779
Dummy-BHT-1-1-1-18
  time_start:1691160821
  time_end:1691160823
```
