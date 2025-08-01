# DBMS

To include a DBMS in a Kubernetes-based experiment you will need
* a Docker Image
* a JDBC Driver
* a Kubernetes Deployment Template
* some configuration
  * How to load data (DDL command)
  * DDL scripts
  * How to connect via JDBC

This document contains examples for
* [MariaDB](#mariadb)
* [MonetDB](#monetdb)
* [PostgreSQL](#postgresql)
* [MySQL](#mysql)


## Example Explained

### Configuration

DBMS can be adressed using a key.
We have to define some data per key, for example for the key `PostgreSQL` we use:

```
'PostgreSQL': {
    'loadData': 'psql -U postgres < {scriptname}',
    'delay_prepare': 60,
    'template': {
        'version': 'v11.4',
        'alias': 'General-B',
        'docker_alias': 'GP-B',
         'JDBC': {
            'driver': "org.postgresql.Driver",
            'auth': ["postgres", ""],
            'url': 'jdbc:postgresql://{serverip}:9091/postgres?reWriteBatchedInserts=true',
            'jar': 'postgresql-42.5.0.jar'
        }
    },
    'logfile': '/usr/local/data/logfile',
    'datadir': '/var/lib/postgresql/data/',
    'priceperhourdollar': 0.0,
},
```
This has
* a base name for the DBMS
* a `delay_prepare` in seconds to wait before system is considered ready
* a placeholder `template` for the [benchmark tool DBMSBenchmarker](https://dbmsbenchmarker.readthedocs.io/en/latest/Options.html#connection-file)  
  Some of the data in the reference, like `hostsystem`, will be added by bexhoma automatically.  
* assumed to have the JDBC driver jar locally available inside the benchmarking tool
* a command `loadData` for running the init scripts  
  Some placeholders in the URL are: `serverip` (set automatically to match the corresponding pod), `dbname`, `DBNAME`, `timout_s`, `timeout_ms` (name of the database in lower and upper case, timeout in seconds and miliseconds)
* `{serverip}` as a placeholder for the host address
* `{dbname}` as a placeholder for the db name
* an optional `priceperhourdollar` (currently ignored)
* an optional name of a `logfile` that is downloaded after the benchmark
* name of the `datadir` of the DBMS. It's size is measured using `du` after data loading has been finished.

### Collect Host Informations

Some information is given by configuration (JDBC data e.g.), some is collected automatically from the experiment host:
```
cluster.get_host_memory()
cluster.get_host_cpu()
cluster.get_host_cores()
cluster.get_host_system()
cluster.get_host_diskspace_used()
cluster.get_host_diskspace_used_data()
cluster.get_host_cuda()
cluster.get_host_gpus()
cluster.get_host_gpu_ids()
cluster.get_host_node()
```

Most of these run inside the docker container:
* `cluster.get_host_memory()`: Collects `grep MemTotal /proc/meminfo | awk '{print $2}'` and multiplies by 1024
* `cluster.get_host_cpu()`: Collects `cat /proc/cpuinfo | grep \'model name\' | head -n 1`
* `cluster.get_host_cores()`: Collects `grep -c ^processor /proc/cpuinfo`
* `cluster.get_host_system()`: Collects `uname -r`
* `cluster.get_host_diskspace_used()`: Collects `df / | awk 'NR == 2{print $3}'`
* `cluster.get_host_diskspace_used_data()`: Collects `du datadir | awk 'END{ FS=OFS=\"\t\" }END{print $1}'` inside docker container, where `datadir` is set in config of DBMS
* `cluster.get_host_cuda()`: Collects `nvidia-smi | grep \'CUDA\'`
* `cluster.get_host_gpus()`: Collects `nvidia-smi -L` and then aggregates the type using `Counter([x[x.find(":")+2:x.find("(")-1] for x in l if len(x)>0])`
* `cluster.get_host_gpu_ids()`: Collects `nvidia-smi -L` and finds 'UUID: ' inside
* `cluster.get_host_node()`: Gets `spec.nodeName` from pod description
* `cluster.get_host_volume()`: Gets size and used from `df -h | grep volumes`

### Deployment Manifests

Every DBMS that is deployed by bexhoma needs a YAML manifest.
See for example https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-PostgreSQL.yml

You may want to pay attention to name of the secret:
```
      imagePullSecrets:
      - {name: dockerhub}
```
Another section that might be interesting is
```
      tolerations:
```

#### Parametrize Templates

Some parameters can be changed per DBMS or per experiment in Python, for example
```
experiment.set_resources(
    requests = {
        'cpu': cpu,
        'memory': memory,
        'gpu': 0
    },
    limits = {
        'cpu': 0,
        'memory': 0
    },
    nodeSelector = {
        'cpu': cpu_type,
        'gpu': '',
    })
experiment.set_resources(
    nodeSelector = {
        'cpu': cpu_type,
        'gpu': '',
        'kubernetes.io/hostname': request_node_name
    })        
```

The parameters can be set via CLI (see for example `tpch.py`).

## MariaDB

### Deployment

https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MariaDB.yml

As of bexhoma version `v0.7.1` this contains
```
        args: [
          "--innodb_log_buffer_size", "17179869184",
          "--innodb-write-io-threads", "16",
          "--innodb-log-file-size", "4294967296"
        ]
```
as default settings.

### Configuration

```
       'MariaDB': {
            'loadData': 'mariadb < {scriptname}',
            'template': {
                'version': 'v10.4.6',
                'alias': 'GP A',
                'docker_alias': 'GP A',
                'dialect': 'MySQL',
                'JDBC': {
                    'driver': "org.mariadb.jdbc.Driver",
                    'auth': ["root", ""],
                    'url': 'jdbc:mysql://{serverip}:9091/{dbname}',
                    'jar': './mariadb-java-client-3.1.0.jar'
                }
            },
            'logfile': '',
            'datadir': '/var/lib/mysql/',
            'priceperhourdollar': 0.0,
        },
```

### DDL Scripts

Example for [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MariaDB)

## MonetDB

### Deployment

https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MonetDB.yml

### Configuration

```
       'MonetDB': {
            'loadData': 'cd /home/monetdb;echo "user=monetdb\npassword=monetdb" > .monetdb;mclient demo < {scriptname}',
            'template': {
                'version': '11.37.11',
                'alias': 'Columnwise',
                'docker_alias': 'Columnwise',
                 'JDBC': {
                    'auth': ['monetdb', 'monetdb'],
                    'driver': 'org.monetdb.jdbc.MonetDriver',
                    'jar': 'jars/monetdb-jdbc-3.3.jre8',
                    'url': 'jdbc:monetdb://{serverip}:9091/demo?so_timeout=0'
                }
            },
            'logfile': '/var/monetdb5/dbfarm/merovingian.log',
            'datadir': '/var/monetdb5/',
            'priceperhourdollar': 0.0,
        },
```

### DDL Scripts

Example for
* [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MonetDB)

## PostgreSQL

### Deployment

https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-PostgreSQL.yml

As of bexhoma version `v0.8.9` this contains
```
        args:
          # --- Connection & Worker Processes ---
          - "-c"
          - "max_connections=1500"       # https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-MAX-CONNECTIONS
          - "-c"
          - "max_worker_processes=128"   # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-WORKER-PROCESSES
          - "-c"
          - "max_parallel_workers=64"    # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS
          - "-c"
          - "max_parallel_workers_per_gather=8"  # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-PARALLEL-WORKERS-PER-GATHER
          - "-c"
          - "max_parallel_maintenance_workers=8" # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-PARALLEL-MAINTENANCE-WORKERS

          # --- Memory Settings ---
          - "-c"
          - "shared_buffers=256GB"       # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-SHARED-BUFFERS
          - "-c"
          - "effective_cache_size=350GB" # https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-EFFECTIVE-CACHE-SIZE
          - "-c"
          - "work_mem=128MB"             # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-WORK-MEM
          - "-c"
          - "maintenance_work_mem=4GB"   # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM
          - "-c"
          - "temp_buffers=64MB"          # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-TEMP-BUFFERS
          - "-c"
          - "wal_buffers=16MB"           # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-BUFFERS
          - "-c"
          - "autovacuum_work_mem=1GB"    # https://www.postgresql.org/docs/current/runtime-config-autovacuum.html#GUC-AUTOVACUUM-WORK-MEM

          # --- Autovacuum ---
          - "-c"
          - "autovacuum=on"                           # https://www.postgresql.org/docs/current/runtime-config-autovacuum.html#GUC-AUTOVACUUM
          - "-c"
          - "autovacuum_max_workers=10"               # https://www.postgresql.org/docs/current/runtime-config-autovacuum.html#GUC-AUTOVACUUM-MAX-WORKERS
          - "-c"
          - "autovacuum_vacuum_cost_limit=1000"       # https://www.postgresql.org/docs/current/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-LIMIT
          - "-c"
          - "vacuum_cost_limit=1000"                  # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-VACUUM-COST-LIMIT
          - "-c"
          - "autovacuum_naptime=15s"                  # https://www.postgresql.org/docs/current/runtime-config-autovacuum.html#GUC-AUTOVACUUM-NAPTIME
          - "-c"
          - "autovacuum_vacuum_cost_delay=20ms"       # https://www.postgresql.org/docs/current/runtime-config-autovacuum.html#GUC-AUTOVACUUM-VACUUM-COST-DELAY

          # --- WAL & Checkpoints (Ceph-optimized) ---
          - "-c"
          - "wal_level=replica"                       # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-LEVEL
          - "-c"
          - "wal_compression=on"                      # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-COMPRESSION
          - "-c"
          - "wal_writer_delay=500ms"                  # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-WRITER-DELAY
          - "-c"
          - "commit_delay=10000"                      # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-COMMIT-DELAY
          - "-c"
          - "synchronous_commit=off"                  # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT
          - "-c"
          - "max_wal_size=2GB"                        # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-MAX-WAL-SIZE
          - "-c"
          - "min_wal_size=1GB"                        # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-MIN-WAL-SIZE
          - "-c"
          - "checkpoint_timeout=5min"                 # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-CHECKPOINT-TIMEOUT
          - "-c"
          - "checkpoint_completion_target=0.9"        # https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-CHECKPOINT-COMPLETION-TARGET

          # --- Planner Cost Tweaks (CephFS) ---
          - "-c"
          - "random_page_cost=4.0"                    # https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-RANDOM-PAGE-COST
          - "-c"
          - "seq_page_cost=1.5"                       # https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-SEQ-PAGE-COST
          - "-c"
          - "cpu_tuple_cost=0.01"                     # https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-CPU-TUPLE-COST
          - "-c"
          - "effective_io_concurrency=2"              # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-EFFECTIVE-IO-CONCURRENCY
          - "-c"
          - "default_statistics_target=500"           # https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-DEFAULT-STATISTICS-TARGET

          # --- Locks and Limits ---
          - "-c"
          - "max_locks_per_transaction=128"           # https://www.postgresql.org/docs/current/runtime-config-locks.html#GUC-MAX-LOCKS-PER-TRANSACTION
          - "-c"
          - "max_pred_locks_per_transaction=128"      # https://www.postgresql.org/docs/current/runtime-config-locks.html#GUC-MAX-PRED-LOCKS-PER-TRANSACTION
          - "-c"
          - "max_stack_depth=7MB"                     # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-STACK-DEPTH
          - "-c"
          - "max_files_per_process=4000"              # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-MAX-FILES-PER-PROCESS

          # --- Miscellaneous ---
          - "-c"
          - "huge_pages=try"                          # https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-HUGE-PAGES
```
as default settings.

### Configuration

```
        'PostgreSQL': {
            'loadData': 'psql -U postgres -d {database} < {scriptname}',
            'delay_prepare': 0,
            'template': {
                'version': 'v11.4',
                'alias': 'General-B',
                'docker_alias': 'GP-B',
                 'JDBC': {
                    'driver': "org.postgresql.Driver",
                    'auth': ["postgres", ""],
                    'url': 'jdbc:postgresql://{serverip}:9091/{database}?reWriteBatchedInserts=true&currentSchema={schema}',
                    'jar': 'postgresql-42.5.0.jar',
                    'database': 'postgres',
                    'schema': 'public',
                }
            },
            'logfile': '/usr/local/data/logfile',
            'datadir': '/var/lib/postgresql/data/',
            'priceperhourdollar': 0.0,
            'monitor': {
                'metrics': {
                    'pg_stat_database_blks_read': {
                        'type': 'application',
                        'active': True,
                        'metric': 'counter',
                        'query': 'sum(pg_stat_database_blks_read{{datname!~"template.*"}})',
                        'title': 'Number of disk blocks read in this database'
                    },
                    'pg_stat_database_blks_hit': {
                        'type': 'application',
                        'active': True,
                        'metric': 'counter',
                        'query': 'sum(pg_stat_database_blks_hit{{datname!~"template.*"}})',
                        'title': 'Number of times disk blocks were found already in the buffer cache'
                    },
                    'cache_hit_ratio': {
                        'type': 'application',
                        'active': True,
                        'metric': 'gauge',
                        'query': 'sum(pg_stat_database_blks_hit{{datname!~"template.*"}})/(sum(pg_stat_database_blks_hit{{datname!~"template.*"}}) + sum(pg_stat_database_blks_read{{datname!~"template.*"}}))',
                        'title': 'Cache hit ratio'
                    },
                }
            },
        },
```

This has additional options:
* `database`: the default database
* `schema`: the default schema
* `loadData` knowns the database via `{database}`. This will be replaced by the default database name or, in case of multi-tenancy, by the database of the tenant.
* `url` knowns the database via `{database}` and the schema via `{schema}`. This will be replaced by the default database name and schema name or, in case of multi-tenancy, by the database or schema of the tenant.
* `monitor`: some application metrics to be collected if `-ma` is activated

### DDL Scripts

Example for
* [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/PostgreSQL)
* [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/PostgreSQL)

## MySQL

### Deployment

https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MySQL.yml

As of bexhoma version `v0.7.0` this contains
```
        args: [
          # Some of these need restart
          # The comments come from 8.3 docs
          # https://dev.mysql.com/doc/refman/8.3/en/optimizing-innodb-logging.html
          # https://dev.mysql.com/doc/refman/8.3/en/innodb-performance-multiple_io_threads.html
          "--innodb-write-io-threads=64",             # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_write_io_threads
          "--innodb-read-io-threads=64",              # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_read_io_threads
          # https://dev.mysql.com/doc/refman/8.3/en/innodb-linux-native-aio.html
          "--innodb-use-native-aio=0",                # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_use_native_aio
          # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_page_size
          # "--innodb-page-size=4K",                  # Small for OLTP or similar to filesystem page size
          # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_buffer_pool_chunk_size
          # To avoid potential performance issues, the number of chunks (innodb_buffer_pool_size / innodb_buffer_pool_chunk_size) should not exceed 1000.
          "--innodb-buffer-pool-chunk-size=500M",     # Small when size of pool changes often
          # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_buffer_pool_instances
          # https://releem.com/docs/mysql-performance-tuning/innodb_buffer_pool_size
          "--innodb-buffer-pool-instances=64",        # Parallelizes reads, but may lock writes
          "--innodb-buffer-pool-size=32G",            # Buffer pool size must always be equal to or a multiple of innodb_buffer_pool_chunk_size * innodb_buffer_pool_instances.
          # https://dev.mysql.com/doc/refman/8.3/en/innodb-configuring-io-capacity.html
          "--innodb-io-capacity=1000",                # Faster SSD assumed
          # https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log-buffer.html
          "--innodb-log-buffer-size=32G",             # The size in bytes of the buffer that InnoDB uses to write to the log files on disk
          "--innodb-redo-log-capacity=8G",            # Defines the amount of disk space occupied by redo log files
          "--innodb-flush-log-at-trx-commit=0",       # The default setting of 1 is required for full ACID compliance. With a setting of 0, logs are written and flushed to disk once per second.
          # https://dev.mysql.com/doc/refman/8.3/en/online-ddl-parallel-thread-configuration.html
          "--innodb-parallel-read-threads=64",        # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_parallel_read_threads
          "--innodb-ddl-threads=64",                  # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_ddl_threads
          "--innodb-ddl-buffer-size=128M",            # https://dev.mysql.com/doc/refman/8.3/en/innodb-parameters.html#sysvar_innodb_ddl_buffer_size
          # https://dev.mysql.com/doc/refman/8.3/en/server-system-variables.html#sysvar_tmp_table_size
          "--tmp-table-size=1GB",                     # Defines the maximum size of internal in-memory temporary tables
          "--max-heap-table-size=1GB",                # Maximum size to which user-created MEMORY tables are permitted to grow
          # https://dev.mysql.com/doc/refman/8.3/en/innodb-doublewrite-buffer.html
          "--innodb-doublewrite=0",
          "--innodb-change-buffer-max-size=50",       # You might increase this value for a MySQL server with heavy insert, update, and delete activity
        ]
```
as default settings. It also runs MySQL 8.4.0 as default. Please visit the official website for explanations about settings, https://dev.mysql.com/doc/refman/8.4/en/mysql-nutshell.html

### Configuration

```
        'MySQL': {
            'loadData': 'mysql --local-infile < {scriptname}',
            'delay_prepare': 300,
            'template': {
                'version': 'CE 8.0.22',
                'alias': 'General-C',
                'docker_alias': 'GP-C',
                'dialect': 'MySQL',
                'JDBC': {
                    'driver': "com.mysql.cj.jdbc.Driver",
                    'auth': ["root", "root"],
                    'url': 'jdbc:mysql://{serverip}:9091/{dbname}?rewriteBatchedStatements=true',
                    'jar': ['mysql-connector-j-8.0.31.jar', 'slf4j-simple-1.7.21.jar']
                }
            },
            'logfile': '/var/log/mysqld.log',
            'datadir': '/var/lib/mysql/',
            'priceperhourdollar': 0.0,
        },
```

This uses `delay_prepare` to make bexhoma wait 5 minutes before starting to query the dbms.
This is because configuring InnoDB takes a while and the server might restart during that period.

### DDL Scripts

Example for
* [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MySQL)
* [YCSB](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ycsb/MySQL)


## Add a new DBMS

Suppose you want to add a new DBMS called `newDBMS`.

You will need to
* add a corresponding section to the dockers part in `cluster.config`.
* add a YAML template for the DBMS component called `k8s/deploymenttemplate-NewDBMS.yml` (just copy `k8s/deploymenttemplate-Dummy.yml`)
* add schema scripts for the DBMS in a subfolder of `experiments/`
* add a section to the Python management script, e.g., `example.py`. Look for  
```
    # add configs
    if args.dbms == "Dummy":
        # Dummy DBMS
        name_format = 'Dummy-{cluster}'
        config = configurations.default(experiment=experiment, docker='Dummy', configuration=name_format.format(cluster=cluster_name), dialect='PostgreSQL', alias='DBMS A1')
        config.loading_finished = True
```  
The parameter `docker='Dummy'` refers to the key in the dockers section in `cluster.config` and the name of the file in `k8s/`.
You may add several DBMS by this way to the same experiment for comparison.
Note that `example.py` contains a line
```
parser.add_argument('-dbms', help='DBMS to run the experiment on', choices=['Dummy'])
```
which filters command line arguments and restricts to adding only one DBMS (you may want to ignore `args.dbms` instead).

If you need a JDBC driver different  from the above, please raise an issue: https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues
