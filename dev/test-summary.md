## Show Summary

### Workload
TPC-DS Queries SF=1
- Type: tpcds
- Duration: 404s
- Code: 1749483645
- This includes the reading queries of TPC-DS.
- This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    - TPC-DS (SF=1) data is loaded and benchmark is executed.
    - Query ordering is Q1 - Q99.
    - All instances use the same query parameters.
    - Timeout per query is 600.
    - Import sets indexes and constraints after loading and recomputes statistics.
    - Experiment uses bexhoma version 0.8.7.
    - Experiment is limited to DBMS ['PostgreSQL'].
    - Import is handled by 1 processes (pods).
    - Loading is fixed to cl-worker19.
    - Benchmarking is fixed to cl-worker19.
    - SUT is fixed to cl-worker11.
    - Loading is tested with [1] threads, split into [1] pods.
    - Benchmarking is tested with [64] threads, split into [1] pods.
    - Benchmarking is run as [1] times the number of benchmarking pods.
    - Experiment is run once.

### Services
- PostgreSQL-BHT-1
    - kubectl --context oidc_ds_cluster port-forward service/bexhoma-sut-postgresql-bht-1-1749483645 9091:9091

### Connections
- PostgreSQL-BHT-1-1-1 uses docker image postgres:16.1
    - RAM:541008568320
    - CPU:AMD Opteron(tm) Processor 6378
    - Cores:64
    - host:5.15.0-140-generic
    - node:cl-worker11
    - disk:379054424
    - datadisk:40
    - requests_cpu:4
    - requests_memory:16Gi
    - eval_parameters
        - code:1749483645

### Errors (failed queries)
|            |   PostgreSQL-BHT-1-1-1 |
|:-----------|-----------------------:|
| TPC-DS Q90 |                      1 |
- TPC-DS Q90
    - PostgreSQL-BHT-1-1-1: numRun 1: : org.postgresql.util.PSQLException: ERROR: division by zero

### Warnings (result mismatch)
No warnings

### Latency of Timer Execution [ms]
|               |   PostgreSQL-BHT-1-1-1 |
|:--------------|-----------------------:|
| TPC-DS Q1     |                  42.52 |
| TPC-DS Q2     |                   6.01 |
| TPC-DS Q3     |                   2.23 |
| TPC-DS Q4     |                   9.52 |
| TPC-DS Q5     |                   8.26 |
| TPC-DS Q6     |                   2.6  |
| TPC-DS Q7     |                   2.17 |
| TPC-DS Q8     |                   3.63 |
| TPC-DS Q9     |                   2.79 |
| TPC-DS Q10    |                   3.73 |
| TPC-DS Q11    |                   3.46 |
| TPC-DS Q12    |                   1.79 |
| TPC-DS Q13    |                   3.55 |
| TPC-DS Q14a+b |                  13.29 |
| TPC-DS Q15    |                   1.66 |
| TPC-DS Q16    |                   3.3  |
| TPC-DS Q17    |                  11.1  |
| TPC-DS Q18    |                   3.54 |
| TPC-DS Q19    |                   2.76 |
| TPC-DS Q20    |                   1.54 |
| TPC-DS Q21    |                   2.84 |
| TPC-DS Q22    |                   1.27 |
| TPC-DS Q23a+b |                   9.65 |
| TPC-DS Q24a+b |                   7.52 |
| TPC-DS Q25    |                  31.01 |
| TPC-DS Q26    |                   2.72 |
| TPC-DS Q27    |                   2.71 |
| TPC-DS Q28    |                1727.67 |
| TPC-DS Q29    |                  16.76 |
| TPC-DS Q30    |                   3.08 |
| TPC-DS Q31    |                   5.75 |
| TPC-DS Q32    |                   2.24 |
| TPC-DS Q33    |                   5.48 |
| TPC-DS Q34    |                   3.07 |
| TPC-DS Q35    |                   5.23 |
| TPC-DS Q36    |                   2.59 |
| TPC-DS Q37    |                   2.87 |
| TPC-DS Q38    |                   3.2  |
| TPC-DS Q39a+b |                   5.15 |
| TPC-DS Q40    |                   3.57 |
| TPC-DS Q41    |                   2.83 |
| TPC-DS Q42    |                   2.43 |
| TPC-DS Q43    |                   2.54 |
| TPC-DS Q44    |                   2.9  |
| TPC-DS Q45    |                   2.75 |
| TPC-DS Q46    |                   2.82 |
| TPC-DS Q47    |                   3.13 |
| TPC-DS Q48    |                   2.62 |
| TPC-DS Q49    |                   4.91 |
| TPC-DS Q50    |                   2.75 |
| TPC-DS Q51    |                   2.7  |
| TPC-DS Q52    |                   1.87 |
| TPC-DS Q53    |                   1.94 |
| TPC-DS Q54    |                   3.61 |
| TPC-DS Q55    |                   1.55 |
| TPC-DS Q56    |                   4.13 |
| TPC-DS Q57    |                   2.86 |
| TPC-DS Q58    |                   4.61 |
| TPC-DS Q59    |                   3.9  |
| TPC-DS Q60    |                   4.75 |
| TPC-DS Q61    |                1892.71 |
| TPC-DS Q62    |                   5.04 |
| TPC-DS Q63    |                   2.33 |
| TPC-DS Q64    |                 127.25 |
| TPC-DS Q65    |                   2.45 |
| TPC-DS Q66    |                   8.81 |
| TPC-DS Q67    |                   2.92 |
| TPC-DS Q68    |                   2.82 |
| TPC-DS Q69    |                   3.18 |
| TPC-DS Q70    |                   2.87 |
| TPC-DS Q71    |                   2.92 |
| TPC-DS Q72    |                   9.34 |
| TPC-DS Q73    |                   2.62 |
| TPC-DS Q74    |                   3.28 |
| TPC-DS Q75    |                   5.72 |
| TPC-DS Q76    |                   2.5  |
| TPC-DS Q77    |                2346.77 |
| TPC-DS Q78    |                   5.14 |
| TPC-DS Q79    |                   2.56 |
| TPC-DS Q80    |                   8.78 |
| TPC-DS Q81    |                   2.5  |
| TPC-DS Q82    |                   1.98 |
| TPC-DS Q83    |                   4.04 |
| TPC-DS Q84    |                   2.37 |
| TPC-DS Q85    |                   9.16 |
| TPC-DS Q86    |                   1.87 |
| TPC-DS Q87    |                   2.48 |
| TPC-DS Q88    |                2952.98 |
| TPC-DS Q89    |                   2.61 |
| TPC-DS Q91    |                   3.7  |
| TPC-DS Q92    |                   2.04 |
| TPC-DS Q93    |                   1.94 |
| TPC-DS Q94    |                   3.02 |
| TPC-DS Q95    |                   3.51 |
| TPC-DS Q96    |                   1.46 |
| TPC-DS Q97    |                   2.09 |
| TPC-DS Q98    |                   1.78 |
| TPC-DS Q99    |                   2.29 |

### Loading [s]
|                      |   timeGenerate |   timeIngesting |   timeSchema |   timeIndex |   timeLoad |
|:---------------------|---------------:|----------------:|-------------:|------------:|-----------:|
| PostgreSQL-BHT-1-1-1 |              0 |               0 |            4 |           7 |         13 |

### Geometric Mean of Medians of Timer Run [s]
| DBMS                 |   Geo Times [s] |
|:---------------------|----------------:|
| PostgreSQL-BHT-1-1-1 |          0.0047 |

### Power@Size ((3600 * SF)/(geo times))
| DBMS                 |   Power@Size [~Q/h] |
|:---------------------|--------------------:|
| PostgreSQL-BHT-1-1-1 |              758176 |

### Throughput@Size ((queries * streams * 3600 * SF)/(span of time))
|                                 |   time [s] |   count |   SF |   Throughput@Size |
|:--------------------------------|-----------:|--------:|-----:|------------------:|
| ('PostgreSQL-BHT-1-1', 1, 1, 1) |         13 |       1 |    1 |             27138 |

### Workflow

#### Actual
- DBMS PostgreSQL-BHT - Pods [[1]]

#### Planned
- DBMS PostgreSQL-BHT-1 - Pods [[1]]

### Tests
- TEST passed: Geo Times [s] contains no 0 or NaN
- TEST passed: Power@Size [~Q/h] contains no 0 or NaN
- TEST passed: Throughput@Size contains no 0 or NaN
- TEST failed: SQL errors
- TEST passed: No SQL warnings
- TEST failed: Workflow not as planned