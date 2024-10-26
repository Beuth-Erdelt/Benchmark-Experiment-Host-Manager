# Bexhoma Tool

Boxhoma comes with a tool `bexperiments` (bexhoma experiments).

```
This tool helps managing running Bexhoma experiments in a Kubernetes cluster.

usage: bexperiments [-h] [-db] [-e EXPERIMENT] [-c CONNECTION] [-v] [-cx CONTEXT] {stop,status,dashboard,localdashboard,localresults,jupyter,master,data,summary}

This tool helps managing running Bexhoma experiments in a Kubernetes cluster.

positional arguments:
  {stop,status,dashboard,localdashboard,localresults,jupyter,master,data,summary}
                        manage experiments: stop, get status, connect to dbms or connect to dashboard

options:
  -h, --help            show this help message and exit
  -db, --debug          dump debug informations
  -e EXPERIMENT, --experiment EXPERIMENT
                        code of experiment
  -c CONNECTION, --connection CONNECTION
                        name of DBMS
  -v, --verbose         gives more details about Kubernetes objects
  -cx CONTEXT, --context CONTEXT
                        context of Kubernetes (for a multi cluster environment), default is current context
```

## Stop Experiment

You can stop an experiment via `bexperiments stop -e 12345678` (remove components).

This means, all components (SUT, loader, monitoring, ...) of an experiment are removed from the cluster.
This does not affect persistent storage.
Note that if you have a Python script running, it may continue to create new components, so you have to manually stop the script, too.

If you leave out the `-e` option, all experiments are stopped.


## Connect to Cluster Dashboard

You can connect to the dashboard in the cluster via `bexperiments dashboard`.

This helps inspecting results stored in the cluster.

You can open dashboard in browser at `http://localhost:8050`.
Alternatively you can open a Jupyter notebook at `http://localhost:8888`.
Password is `admin`.


## Connect to Local Dashboard

You can connect to a local dashboard via `bexperiments localdashboard`.

This helps inspecting results stored on the local disk of the orchestrator.

You can open dashboard in browser at `http://localhost:8050`.


## Connect to Local Juypter

You can connect to a local dashboard via `bexperiments jupyter`.

This helps inspecting results stored on the local disk of the orchestrator.

You can open Jupyter notebook in browser at `http://localhost:8888`.
Password is `admin`.


## Connect to Running DBMS

You can connect to a SUT in the cluster via `bexperiments master -e 12345678 -c PostgreSQL`.

It is then available at `localhost:9091`.


## Status Database and Benchmark

You can watch the status of experiments via `bexperiments status`.



```
Dashboard: Running
Message Queue: Running
Data directory: Running
Result directory: Running
Cluster Prometheus: Running
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| Volumes                                  | configuration   | experiment    | loaded [s]   |   timeLoading [s] | dbms       | storage_class_name   | storage   | status   | size   | used   |
+==========================================+=================+===============+==============+===================+============+======================+===========+==========+========+========+
| bexhoma-storage-mariadb-benchbase-16     | mariadb         | benchbase-16  | True         |               326 | MariaDB    | shared               | 50Gi      | Bound    | 50G    | 2.2G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mariadb-hammerdb-16      | mariadb         | hammerdb-16   | True         |               251 | MariaDB    | shared               | 30Gi      | Bound    | 30G    | 2.0G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mariadb-tpch-1           | mariadb         | tpch-1        | True         |              2968 | MariaDB    | shared               | 30Gi      | Bound    | 30G    | 2.0G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mariadb-ycsb-10          | mariadb         | ycsb-10       | True         |             12875 | MariaDB    | shared               | 100Gi     | Bound    | 100G   | 19G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpcds-3          | monetdb         | tpcds-3       | True         |               393 | MonetDB    | shared               | 100Gi     | Bound    | 100G   | 5.4G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpcds-100        | monetdb         | tpcds-100     | True         |              8096 | MonetDB    | shared               | 300Gi     | Bound    | 0      | 0      |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpch-3           | monetdb         | tpch-3        | True         |               215 | MonetDB    | shared               | 100Gi     | Bound    | 100G   | 6.2G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpch-10          | monetdb         | tpch-10       | True         |               576 | MonetDB    | shared               | 100Gi     | Bound    | 100G   | 21G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpch-30          | monetdb         | tpch-30       | True         |              1734 | MonetDB    | shared               | 150Gi     | Bound    | 150G   | 63G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-monetdb-tpch-100         | monetdb         | tpch-100      | True         |              7061 | MonetDB    | shared               | 300Gi     | Bound    | 300G   | 210G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mysql-benchbase-16       | mysql           | benchbase-16  | True         |              3588 | MySQL      | shared               | 50Gi      | Bound    | 50G    | 12G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mysql-hammerdb-16        | mysql           | hammerdb-16   | True         |              2806 | MySQL      | shared               | 30Gi      | Bound    | 30G    | 16G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mysql-tpch-1             | mysql           | tpch-1        | True         |              2178 | MySQL      | shared               | 30Gi      | Bound    | 30G    | 11G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mysql-tpch-10            | mysql           | tpch-10       | True         |             33932 | MySQL      | shared               | 150Gi     | Bound    | 150G   | 36G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-mysql-ycsb-1             | mysql           | ycsb-1        | True         |              4372 | MySQL      | shared               | 100Gi     | Bound    | 100G   | 24G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-benchbase-16  | postgresql      | benchbase-16  | True         |               125 | PostgreSQL | shared               | 50Gi      | Bound    | 50G    | 4.9G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-benchbase-128 | postgresql      | benchbase-128 | True         |              1679 | PostgreSQL | shared               | 200Gi     | Bound    | 200G   | 21G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-hammerdb-16   | postgresql      | hammerdb-16   | True         |               106 | PostgreSQL | shared               | 30Gi      | Bound    | 30G    | 4.8G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-hammerdb-128  | postgresql      | hammerdb-128  | True         |               369 | PostgreSQL | shared               | 50Gi      | Bound    | 50G    | 43G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-tpch-3        | postgresql      | tpch-3        | True         |               300 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 8.0G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-tpch-10       | postgresql      | tpch-10       | True         |              2581 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 17G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-tpch-30       | postgresql      | tpch-30       | True         |             10073 | PostgreSQL | shared               | 150Gi     | Bound    | 150G   | 76G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-ycsb-1        | postgresql      | ycsb-1        | True         |                16 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 3.7G   |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
| bexhoma-storage-postgresql-ycsb-10       | postgresql      | ycsb-10       | True         |               217 | PostgreSQL | shared               | 100Gi     | Bound    | 100G   | 33G    |
+------------------------------------------+-----------------+---------------+--------------+-------------------+------------+----------------------+-----------+----------+--------+--------+
```

## List local results

You can inspect a preview list of results via `bexperiments localresults`.

```
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
|   index    |         name         |                                                                                           info |                       intro                       | queries | connections |         time        |
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
| 1708411664 | TPC-H Queries SF=100 | This experiment compares run time and resource consumption of TPC-H queries in different DBMS. |    This includes the reading queries of TPC-H.    |    22   |      28     | 2024-02-20 11:37:30 |
|            |                      |                                TPC-H data is loaded from a filesystem using several processes. |                                                   |         |             |                     |
|            |                      |                                                             Import is limited to DBMS MonetDB. |                                                   |         |             |                     |
|            |                      |                                                              Import is handled by 1 processes. |                                                   |         |             |                     |
|            |                      |                                                               Loading is fixed to cl-worker19. |                                                   |         |             |                     |
|            |                      |                                                          Benchmarking is fixed to cl-worker19. |                                                   |         |             |                     |
+------------+----------------------+------------------------------------------------------------------------------------------------+---------------------------------------------------+---------+-------------+---------------------+
```


## Status Data Disk

You can watch the status of the data disk via `bexperiments data`.

In the following example output we see we have generated TPC-H at SF=100 using 8 generators.
The data set is split into 8 parts, each of about 14G size.
In total the data set has a size of 106G.

```bash
14G     /data/tpch/SF100/8/8
14G     /data/tpch/SF100/8/3
14G     /data/tpch/SF100/8/2
14G     /data/tpch/SF100/8/4
14G     /data/tpch/SF100/8/1
14G     /data/tpch/SF100/8/5
14G     /data/tpch/SF100/8/7
14G     /data/tpch/SF100/8/6
106G    /data/tpch/SF100/8
106G    /data/tpch/SF100
```


## Inspect Result

You can see the summary of an experiment via `bexperiments summary -e 12345678`.
