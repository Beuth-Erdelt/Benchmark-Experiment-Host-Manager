# Bexhoma Tool

`bexhoma` is the CLI for managing running experiments in a Kubernetes cluster: stopping
components, checking status, inspecting results, and connecting to dashboards or a
running DBMS.
It also dispatches to root-level benchmark scripts, e.g. `bexhoma tpch run`.

```
usage: bexhoma [-h] [-db] [-fe] [-e EXPERIMENT] [-c CONNECTION] [-v] [-cx CONTEXT]
               {stop,status,dashboard,messagequeue,localdashboard,localresults,jupyter,master,data,summary}
               [{start,shutdown}]

options:
  -h, --help            show this help message and exit
  -db, --debug          dump debug information
  -fe, --force-evaluate force a re-evaluation of the results (used with summary)
  -e, --experiment      code of experiment
  -c, --connection      name of DBMS
  -v, --verbose         show more details about Kubernetes objects (used with status)
  -cx, --context        Kubernetes context to use (default: current context)
```

| Command | Purpose |
|---|---|
| `stop [-e CODE]` | Remove an experiment's components (SUT, loader, monitoring, ...) from the cluster. Without `-e`, stops everything. Does not touch persistent storage. |
| `status [-v]` | Show cluster health and per-experiment/per-component status. `-v` adds full Kubernetes object detail. |
| `dashboard` | Port-forward the in-cluster dashboard and Jupyter notebook for inspecting results stored in the cluster. |
| `dashboard start` | Start the dashboard component if it isn't already running. |
| `dashboard shutdown` | Stop the dashboard component. |
| `messagequeue` / `messagequeue start` | Start the message-queue component if it isn't already running. |
| `messagequeue shutdown` | Stop the message-queue component. |
| `localdashboard` | Same dashboard UI, backed by results on the orchestrator's local disk. |
| `jupyter` | Start a local Jupyter notebook over local-disk results. |
| `localresults` | Print a preview table of local results. |
| `data` | Print disk usage of the cluster's data directory. |
| `master -e CODE -c DBMS` | Port-forward a running SUT so it's reachable locally. |
| `summary -e CODE [-fe]` | Print an experiment's results summary; `-fe` forces re-evaluation first. |

## stop

`bexhoma stop -e 12345678` removes all components of experiment `12345678`. If a driving
Python script for that experiment is still running, stop it too — otherwise it keeps
creating new components after they've been removed.

## status

`bexhoma status` reports cluster-level health, then a table of storage volumes, then one
table per running experiment showing each component's state:

```
Dashboard: Running
Message Queue: Running
Data directory: Running
Result directory: Running
Cluster Prometheus: Running
+---------------------------------------+---------------+------------+------------+----------+--------+
| Volumes                               | configuration | experiment | dbms       | status   | used   |
+========================================+===============+============+============+==========+========+
| bexhoma-storage-postgresql-tpch-10     | postgresql    | tpch-10    | PostgreSQL | Bound    | 17G    |
+---------------------------------------+---------------+------------+------------+----------+--------+
| bexhoma-storage-monetdb-tpch-100       | monetdb       | tpch-100   | MonetDB    | Bound    | 210G   |
+---------------------------------------+---------------+------------+------------+----------+--------+
```

The real table also includes `loaded`, `timeLoading`, `storage_class_name`, `storage` and
`size` per volume; `-v` additionally lists Deployments, StatefulSets, Services and Jobs.

## dashboard / localdashboard / jupyter

`bexhoma dashboard` forwards the in-cluster dashboard to `http://localhost:8050` and a
Jupyter notebook to `http://localhost:8888` (password `admin`) — use it to inspect
results stored in the cluster.

`bexhoma dashboard start` deploys the dashboard component if it isn't already running,
without forwarding any ports. `bexhoma dashboard shutdown` removes it.

`bexhoma localdashboard` opens the same dashboard at `http://localhost:8050`, but reading
results from the orchestrator's local disk instead.

`bexhoma jupyter` starts a local Jupyter notebook (`http://localhost:8888`, password
`admin`) over the same local-disk results.

## messagequeue

`bexhoma messagequeue` (equivalently `bexhoma messagequeue start`) deploys the message
queue used to coordinate loader/benchmarker pods, if it isn't already running.
`bexhoma messagequeue shutdown` removes it.

## localresults

`bexhoma localresults` prints a preview table of local results (name, description, query
count, connection count, timestamp):

```
+------------+----------------------+-------------------------------------------------+---------+-------------+---------------------+
|   index    |         name         |                       info                       | queries | connections |         time        |
+------------+----------------------+-------------------------------------------------+---------+-------------+---------------------+
| 1708411664 | TPC-H Queries SF=100 | Compares run time and resource use across DBMS.  |    22   |      28     | 2024-02-20 11:37:30 |
+------------+----------------------+-------------------------------------------------+---------+-------------+---------------------+
```

## data

`bexhoma data` prints `du -h` of the cluster's data directory, e.g. a TPC-H SF=100 data
set generated by 8 parallel generators, split into 8 parts of ~14G each:

```bash
14G     /data/tpch/SF100/8/1
...
106G    /data/tpch/SF100/8
106G    /data/tpch/SF100
```

## master

`bexhoma master -e 12345678 -c PostgreSQL` port-forwards the named SUT of an experiment
so it's reachable at `localhost:9091`.

`-e` and `-c` are optional filters, not required selectors: omitting either widens the
Kubernetes label selector, and the first matching SUT Service found is the one forwarded.
If exactly one SUT is running cluster-wide, leaving both out "just works" — but if several
are running, you get whichever one the Kubernetes API happens to return first, with no
warning about the ambiguity. Pass `-e`/`-c` explicitly whenever more than one SUT may be
running.

## summary

`bexhoma summary -e 12345678` prints the results summary of an experiment. Add `-fe` to
force re-evaluation of stored results before printing.
