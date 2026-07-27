## Show Summary

### Workload
TPC-H Queries SF=100
* Type: tpch
* Duration: 5539s 
* Code: 1785155487
* This includes the reading queries of TPC-H.
* This experiment compares run time and resource consumption of TPC-H queries in different DBMS.
  * TPC-H (SF=100) data is loaded and benchmark is executed.
  * Query ordering is Q1 - Q22.
  * All instances use the same query parameters.
  * Timeout per query is 3600.
  * Data transfer volume per query is also measured.
  * Import sets indexes and constraints after loading and recomputes statistics.
  * Experiment uses bexhoma version 0.10.8.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['MonetDB'].
  * Import is handled by 8 processes (pods).
  * Loading is fixed to cl-worker19.
  * Benchmarking is fixed to cl-worker19.
  * Database is persisted to disk of type shared and size 1000Gi. Persistent storage is removed at experiment start.
  * Loading is tested with [8] threads, split into [8] pods.
  * Benchmarking is tested with [1] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * SUT requests 16 CPU and 256Gi RAM. CPU limit is 16. RAM limit is 256Gi.

### Connections
* MonetDB-1-1-1-1-1 uses docker image monetdb/monetdb:Dec2025-SP3
  * RAM:2164173213696
  * CPU:INTEL(R) XEON(R) PLATINUM 8570
  * Cores:224
  * host:6.8.0-111-generic
  * node:cl-worker36
  * disk:811355
  * volume_size:1000G
  * volume_used:183G
  * cpu_list:0-223
  * requests_cpu:16
  * requests_memory:256Gi
  * limits_cpu:16
  * limits_memory:256Gi
  * eval_parameters
    * code:1785155487

### SUT Container Restarts
* bexhoma-sut-monetdb-1-1785155487-74988b4bdc-wbbzw: 0

### Workflow

#### Actual

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

#### Planned

* DBMS MonetDB-1 - Experiment 1 Client 1: tpch (1 pods)

### Loading

#### Per Run

|             |   experiment_run |   SF |   time_load |   time_preload |   time_generate |   time_ingest |   time_postload |   loading_pods |   terminals | tenant_id   | type_tenants   |   num_tenants | vol_tenants   |   Throughput [SF/h] |
|:------------|-----------------:|-----:|------------:|---------------:|----------------:|--------------:|----------------:|---------------:|------------:|:------------|:---------------|--------------:|:--------------|--------------------:|
| MonetDB-1-1 |                1 |  100 |     6824.00 |           4.00 |           14.00 |       2235.00 |         4565.00 |              8 |           0 |             | None           |             0 | False         |               52.75 |

### Execution

#### Per Connection

| DBMS              | configuration   | phase         | job             |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id | pod               |
|:------------------|:----------------|:--------------|:----------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|:------------------|
| MonetDB-1-1-1-1-1 | MonetDB-1       | MonetDB-1-1-1 | MonetDB-1-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |        707 |           17.30 |            21765.77 |          11202.26 |          -1 | MonetDB-1-1-1-1-1 |

#### Per Phase

|               | phase         |   experiment_run |   client |   benchmark_run |   pod_count |     SF |   num_of_queries |   time [s] |   Geo Times [s] |   Power@Size [~Q/h] |   Throughput@Size |   tenant_id |
|:--------------|:--------------|-----------------:|---------:|----------------:|------------:|-------:|-----------------:|-----------:|----------------:|--------------------:|------------------:|------------:|
| MonetDB-1-1-1 | MonetDB-1-1-1 |                1 |        1 |               1 |           1 | 100.00 |               22 |        707 |           17.30 |            21765.77 |          11202.26 |          -1 |

### Latency of Timer Execution [ms]
| Queries                                             |   MonetDB-1-1-1-1-1 |
|:----------------------------------------------------|--------------------:|
| Pricing Summary Report (TPC-H Q1)                   |            98672.54 |
| Minimum Cost Supplier Query (TPC-H Q2)              |             2355.96 |
| Shipping Priority (TPC-H Q3)                        |            37846.39 |
| Order Priority Checking Query (TPC-H Q4)            |            16974.82 |
| Local Supplier Volume (TPC-H Q5)                    |            24327.80 |
| Forecasting Revenue Change (TPC-H Q6)               |            26091.34 |
| Volume Shipping Query (TPC-H Q7)                    |            18426.24 |
| National Market Share (TPC-H Q8)                    |            20119.62 |
| Product Type Profit Measure (TPC-H Q9)              |            47047.65 |
| Returned Item Reporting Query (TPC-H Q10)           |             7162.88 |
| Important Stock Identification (TPC-H Q11)          |             2330.37 |
| Shipping Modes and Order Priority (TPC-H Q12)       |            12487.48 |
| Customer Distribution (TPC-H Q13)                   |            35757.38 |
| Promotion Effect Query (TPC-H Q14)                  |            22781.53 |
| Top Supplier Query (TPC-H Q15)                      |             7387.05 |
| Parts/Supplier Relationship (TPC-H Q16)             |             4449.95 |
| Small-Quantity-Order Revenue (TPC-H Q17)            |             9766.57 |
| Large Volume Customer (TPC-H Q18)                   |            24039.98 |
| Discounted Revenue (TPC-H Q19)                      |            26897.09 |
| Potential Part Promotion (TPC-H Q20)                |            15160.26 |
| Suppliers Who Kept Orders Waiting Query (TPC-H Q21) |           221138.75 |
| Global Sales Opportunity Query (TPC-H Q22)          |             3286.42 |

### Errors (failed queries)

No errors

### Warnings (result mismatch)

No warnings

### Monitoring

### Loading phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      8572.25 |      4.61 |         185.36 |                185.36 |

### Loading phase: component data generator

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |         0.00 |      0.00 |           0.00 |                  0.00 |

### Loading phase: component loader

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      1899.80 |      1.27 |           0.03 |                 13.29 |

### Execution phase: SUT deployment

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |      4921.86 |     15.67 |         247.40 |                247.40 |

### Execution phase: component benchmarker

| DBMS            |   CPU [CPUs] |   Max CPU |   Max RAM [Gb] |   Max RAM Cached [Gb] |
|:----------------|-------------:|----------:|---------------:|----------------------:|
| MonetDB-1-1-1-1 |        34.11 |      0.29 |           0.38 |                  0.39 |

### Tests
* TEST passed: No SUT container restarts
* TEST passed: Loading phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST skipped: Loading phase: component data generator contains 0 or NaN in CPU [CPUs] (data pre-existing)
* TEST passed: Loading phase: component loader contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: SUT deployment contains no 0 or NaN in CPU [CPUs]
* TEST passed: Execution phase: component benchmarker contains no 0 or NaN in CPU [CPUs]
* TEST passed: Geo Times [s] contains no 0 or NaN
* TEST passed: Power@Size [~Q/h] contains no 0 or NaN
* TEST passed: Throughput@Size contains no 0 or NaN
* TEST passed: No SQL errors
* TEST passed: No SQL warnings
* TEST passed: Workflow as planned
