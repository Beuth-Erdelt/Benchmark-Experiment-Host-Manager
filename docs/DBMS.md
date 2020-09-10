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
* [OmniSci](#omnisci)
* [PostgreSQL](#postgresql)


## Example Explained

### Deployment

See documentation of [deployments](Deployments.md).

### Configuration

```
'dockers': {
    'OmniSci': {
        'loadData': 'bin/omnisql -u admin -pHyperInteractive < {scriptname}',     # DBMS: Command to Login and Run Scripts
        'template': {                                                             # Template for Benchmark Tool
            'version': 'CE v5.4',
            'alias': 'GPU',
            'docker_alias': 'GPU',
            'JDBC': {
                'driver': 'com.omnisci.jdbc.OmniSciDriver',
                'url': 'jdbc:omnisci:{serverip}:9091:omnisci',
                'auth': {'user': 'admin', 'password': 'HyperInteractive'},
                'jar': './omnisci-jdbc-4.7.1.jar'                                   # DBMS: Local Path to JDBC Jar
            }
        },
        'logfile': '/omnisci-storage/data/mapd_log/omnisci_server.INFO',          # DBMS: Path to Log File on Server
        'datadir': '/omnisci-storage/data/mapd_data/',                            # DBMS: Path to directory containing data storage
        'priceperhourdollar': 0.0,                                                # DBMS: Price per hour in USD if DBMS is rented
    }
}
```
This has
* a base name for the DBMS
* a placeholder `template` for the [benchmark tool](https://github.com/Beuth-Erdelt/DBMS-Benchmarker/blob/master/docs/Options.md#connection-file)
* the JDBC driver jar locally available
* a command `loadData` for running the init scripts with `{scriptname}` as a placeholder for the script name inside the container
* `{serverip}` as a placeholder for the host address (localhost for k8s, an Elastic IP for AWS)
* `{dbname}` as a placeholder for the db name
* an optional `priceperhourdollar`
* an optional name of a `logfile` that is downloaded after the benchmark
* name of the `datadir` of the DBMS. It's size is measured using `du` after data loading has been finished.

## MariaDB

**Deployment**

https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MariaDB.yml

**Configuration**
```
       'MariaDB': {
            'loadData': 'mysql < {scriptname}',
            'template': {
                'version': 'v10.4.6',
                'alias': 'GP A',
                'docker_alias': 'GP A',
                'dialect': 'MySQL',
                'JDBC': {
                    'driver': "org.mariadb.jdbc.Driver",
                    'auth': ["root", ""],
                    'url': 'jdbc:mysql://{serverip}:9091/{dbname}',
                    'jar': './mariadb-java-client-2.3.0.jar'
                }
            },
            'logfile': '',
            'datadir': '/var/lib/mysql/',
            'priceperhourdollar': 0.0,
        },
```

***DDL Scripts***

Example for [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MariaDB)

## MonetDB

**Deployment**

https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-MonetDB.yml

**Configuration**
```
       'MonetDB': {
            'loadData': 'cd /home/monetdb;mclient db < {scriptname}',
            'template': {
                'version': 'v11.31.7',
                'alias': 'In-Memory C',
                'docker_alias': 'In-Memory C',
                 'JDBC': {
                    'auth': ['monetdb', 'monetdb'],
                    'driver': 'nl.cwi.monetdb.jdbc.MonetDriver',
                    'jar': './monetdb-jdbc-2.29.jar',
                    'url': 'jdbc:monetdb://{serverip}:9091/db'
                }
            },
            'logfile': '',
            'datadir': '/var/monetdb5/',
            'priceperhourdollar': 0.0,
        },
```

***DDL Scripts***

Example for [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/MonetDB)

## OmniSci

**Deployment**

https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-OmniSci.yml

**Configuration**
```
        'OmniSci': {
            'loadData': 'bin/omnisql -u admin -pHyperInteractive < {scriptname}',
            'template': {
                'version': 'CE v4.7',
                'alias': 'GPU A',
                'docker_alias': 'GPU A',
                'JDBC': {
                    'driver': 'com.omnisci.jdbc.OmniSciDriver',
                    'url': 'jdbc:omnisci:{serverip}:9091:omnisci',
                    'auth': {'user': 'admin', 'password': 'HyperInteractive'},
                    'jar': './omnisci-jdbc-4.7.1.jar'
                }
            },
            'logfile': '/omnisci-storage/data/mapd_log/omnisci_server.INFO',
            'datadir': '/omnisci-storage/',
            'priceperhourdollar': 0.0,
        },
```

***DDL Scripts***

Example for [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/OmniSci)

## PostgreSQL

**Deployment**

https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-PostgreSQL.yml

**Configuration**

```
        'PostgreSQL': {
            'loadData': 'psql -U postgres < {scriptname}',
            'template': {
                'version': 'v11.4',
                'alias': 'GP D',
                'docker_alias': 'GP D',
                'JDBC': {
                    'driver': "org.postgresql.Driver",
                    'auth': ["postgres", ""],
                    'url': 'jdbc:postgresql://{serverip}:9091/postgres',
                    'jar': './postgresql-42.2.5.jar'
                }
            },
            'logfile': '',
            'datadir': '/var/lib/postgresql/data/',
            'priceperhourdollar': 0.0,
        },
```

***DDL Scripts***

Example for [TPC-H](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/tpch/PostgreSQL)
