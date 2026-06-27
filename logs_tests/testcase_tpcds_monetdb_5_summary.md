## Show Summary

### Workload
TPC-DS Queries SF=100
    Type: tpcds
    Duration: 20752s 
    Code: 1729497306
    This includes the reading queries of TPC-DS.
    This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.
    TPC-DS (SF=100) data is loaded and benchmark is executed.
    Query ordering is Q1 - Q99.
    All instances use the same query parameters.
    Import sets indexes and constraints after loading and recomputes statistics.
    System metrics are monitored by a cluster-wide installation.
    Benchmark is limited to DBMS ['MonetDB'].
    Import is handled by 8 processes (pods).
    Loading is fixed to cl-worker19.
    Benchmarking is fixed to cl-worker19.
    SUT is fixed to cl-worker11.
    Database is persisted to disk of type shared and size 300Gi.
    Loading is tested with [8] threads, split into [8] pods.
    Benchmarking is tested with [1] threads, split into [1] pods.
    Benchmarking is run as [1, 1, 5, 5] times the number of benchmarking pods.
    Experiment is run once.

### Connections
MonetDB-BHT-8-1-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250321764
    datadisk:288744504
    volume_size:300G
    volume_used:276G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-2-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322104
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-4 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-3-5 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322276
    datadisk:157561721
    volume_size:300G
    volume_used:151G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-1 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-2 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-3 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-4 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi
MonetDB-BHT-8-4-5 uses docker image monetdb/monetdb:Dec2023
    RAM:541008605184
    CPU:AMD Opteron(tm) Processor 6378
    Cores:64
    host:5.15.0-116-generic
    node:cl-worker11
    disk:250322616
    datadisk:232899461
    volume_size:300G
    volume_used:223G
    requests_cpu:4
    requests_memory:16Gi

### Errors (failed queries)
               MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q23a+b              False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q24a+b              False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q25                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q26                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q27                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q28                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q29                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q30                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q31                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q32                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q33                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q34                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q35                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q37                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q38                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q39a+b              False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q40                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q41                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q42                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q43                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q44                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q45                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q46                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q47                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q48                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q49                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q50                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q51                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q52                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q53                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q54                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q55                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q56                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q57                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q58                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q59                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q60                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q61                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q62                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q63                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q64                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q65                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q66                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q67                 False              False               True              False               True              False              False              False              False              False               True              False
TPC-DS Q68                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q69                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q71                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q72                 False              False               True               True               True              False              False              False              False              False               True              False
TPC-DS Q73                 False              False               True               True               True              False              False              False               True               True               True              False
TPC-DS Q74                 False              False               True               True               True              False              False              False               True               True               True              False
TPC-DS Q75                 False              False               True               True               True              False              False              False               True               True               True               True
TPC-DS Q76                 False              False               True               True               True              False              False               True               True               True               True               True
TPC-DS Q77                 False              False               True               True               True              False              False               True               True               True               True               True
TPC-DS Q78                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q79                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q80                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q81                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q82                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q83                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q84                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q85                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q87                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q88                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q89                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q90                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q91                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q92                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q93                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q94                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q95                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q96                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q97                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q98                 False              False               True               True               True               True               True               True               True               True               True               True
TPC-DS Q99                 False              False               True               True               True               True               True               True               True               True               True               True

### Warnings (result mismatch)
            MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q1                True               True               True              False               True               True               True               True               True               True               True               True
TPC-DS Q34               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q46               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q54               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q68               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q69               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q71               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q72               True               True              False              False              False               True               True               True               True               True              False               True
TPC-DS Q73               True               True              False              False              False               True               True               True              False              False              False               True
TPC-DS Q74               True               True              False              False              False               True               True               True              False              False              False               True
TPC-DS Q75               True               True              False              False              False               True               True               True              False              False              False              False
TPC-DS Q76               True               True              False              False              False               True               True              False              False              False              False              False
TPC-DS Q77               True               True              False              False              False               True               True              False              False              False              False              False
TPC-DS Q78               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q79               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q80               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q81               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q82               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q83               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q84               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q85               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q87               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q88               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q89               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q90               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q91               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q92               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q93               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q94               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q95               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q96               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q97               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q98               True               True              False              False              False              False              False              False              False              False              False              False
TPC-DS Q99               True               True              False              False              False              False              False              False              False              False              False              False

### Latency of Timer Execution [ms]
DBMS           MonetDB-BHT-8-1-1  MonetDB-BHT-8-2-1  MonetDB-BHT-8-3-1  MonetDB-BHT-8-3-2  MonetDB-BHT-8-3-3  MonetDB-BHT-8-3-4  MonetDB-BHT-8-3-5  MonetDB-BHT-8-4-1  MonetDB-BHT-8-4-2  MonetDB-BHT-8-4-3  MonetDB-BHT-8-4-4  MonetDB-BHT-8-4-5
TPC-DS Q1               27370.75            2398.34            3427.48            3548.13            2621.80            3349.98            2533.30           42994.62           43099.49           42921.18           42831.04           42908.51
TPC-DS Q2              290821.48           12968.89           42420.72           43545.27           43077.55           42017.09           43019.55          587520.51          587142.92          589163.04          587448.87          588656.35
TPC-DS Q3              113297.32            2534.75            2226.94            1311.94            2827.32            2754.30            2898.16          126104.75          126592.93          124695.38          126524.33          125210.92
TPC-DS Q4              419012.49          151417.82          841027.33          841979.72          771544.18          758497.43          987181.05          863825.28          842226.46          875548.69          841795.93          864986.88
TPC-DS Q5              152472.27           25913.86           38700.56           38704.71           75992.76           89474.50           35704.63          280847.09          302657.12          272871.72          309269.37          290256.00
TPC-DS Q6               10465.72            6148.11            8494.14            8372.64           20295.71           19794.75           10755.25           39960.65           38099.00           35536.35           36848.37           32571.94
TPC-DS Q7               85464.02            1717.00             656.49             659.43           14569.19           14941.80             779.82          125905.42          127393.38          126724.35          122928.01          123021.42
TPC-DS Q8               31537.49            2868.56           51567.86           50598.40           57879.85           57629.18            4131.33           37375.11           37821.85           37375.05           37374.59           37374.76
TPC-DS Q9               24558.10            2959.41            9601.51            7915.98            8954.79            8555.44            2609.90           39832.01           37006.15           39783.22           39745.52           39686.99
TPC-DS Q10               4798.43            1708.85           10055.94           12059.05           11024.65           11410.25            1068.77            8830.09           11203.75            8863.00            8856.28            8982.50
TPC-DS Q11              74948.80           74442.53          127970.28          129086.83          119531.67          127820.74           98889.67          128465.69          116448.46          123230.43          115624.77          126471.84
TPC-DS Q12               1922.56             586.98             489.47             429.42            8194.10             615.13             359.98             302.72             711.24            3474.69            1657.43             523.10
TPC-DS Q13               2705.39            1601.06            3541.62            2587.14            4190.26            3541.01             356.11             335.97            8615.20             375.12            8625.05             414.59
TPC-DS Q14a+b          331389.83          274582.58          495565.35          450771.53          450517.42          450518.97          498161.82          544996.30          520469.11          543487.22          534403.23          570664.29
TPC-DS Q15              11234.26            1133.29             539.39            3274.29            3533.18            3535.34             704.67             639.50           14143.56             606.52             869.53            1274.78
TPC-DS Q16              25139.98             863.51             783.43            5917.83            5936.80            5181.27             795.14           43898.62           57727.55           46832.57           57696.69           19303.74
TPC-DS Q17              57273.54           34438.89          136125.32          173456.87          179543.43          175108.63           85005.01          218938.52          223817.53          219048.18          220848.61          219440.73
TPC-DS Q18              26480.21            8663.66           22465.62           22848.76           15768.86           21216.73           21039.15           51344.16           46580.72           51222.66           49248.84           50783.59
TPC-DS Q19               2424.20            2259.17            6801.66            6127.00            6794.42            6798.48            6977.89            9677.23            9660.20            9704.29            9707.72            9694.76
TPC-DS Q20                941.11             498.07             859.07             876.10            1179.98            1178.25            1177.47             731.59             729.09             735.39             730.50             730.95
TPC-DS Q21             115406.12             950.95            6428.35            6422.47            6412.70            6404.55            6426.69          142631.61          142621.07          142619.30          142613.04          142602.51
TPC-DS Q22              91135.38           81955.21           97082.60          112905.33          112828.09          107411.61           97016.26           97696.66          110253.74           97281.24           91222.80          121667.95

### Loading [s]
                   timeGenerate  timeIngesting  timeSchema  timeIndex  timeLoad
MonetDB-BHT-8-1-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-2-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-2        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-3        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-4        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-3-5        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-1        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-2        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-3        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-4        4023.0         1362.0         6.0     2703.0    8096.0
MonetDB-BHT-8-4-5        4023.0         1362.0         6.0     2703.0    8096.0

### Geometric Mean of Medians of Timer Run [s]
                   Geo Times [s]
DBMS                            
MonetDB-BHT-8-1-1          29.76
MonetDB-BHT-8-2-1           5.57
MonetDB-BHT-8-3-1          11.35
MonetDB-BHT-8-3-2          13.07
MonetDB-BHT-8-3-3          19.37
MonetDB-BHT-8-3-4          17.48
MonetDB-BHT-8-3-5           7.76
MonetDB-BHT-8-4-1          35.40
MonetDB-BHT-8-4-2          49.88
MonetDB-BHT-8-4-3          39.40
MonetDB-BHT-8-4-4          44.92
MonetDB-BHT-8-4-5          36.51

### Power@Size
                   Power@Size [~Q/h]
DBMS                                
MonetDB-BHT-8-1-1           12115.25
MonetDB-BHT-8-2-1           64912.63
MonetDB-BHT-8-3-1           31815.26
MonetDB-BHT-8-3-2           27619.23
MonetDB-BHT-8-3-3           18609.96
MonetDB-BHT-8-3-4           20642.87
MonetDB-BHT-8-3-5           46558.91
MonetDB-BHT-8-4-1           10194.85
MonetDB-BHT-8-4-2            7229.98
MonetDB-BHT-8-4-3            9147.06
MonetDB-BHT-8-4-4            8024.32
MonetDB-BHT-8-4-5            9884.43

### Throughput@Size
                                               time [s]  count   SF  Throughput@Size [~GB/h]
DBMS            SF  num_experiment num_client                                               
MonetDB-BHT-8-1 100 1              1               6889      1  100                  1149.66
MonetDB-BHT-8-2 100 1              2               3711      1  100                  2134.20
MonetDB-BHT-8-3 100 1              3               4040      5  100                  9801.98
MonetDB-BHT-8-4 100 1              4               5477      5  100                  7230.24

### Workflow

#### Actual
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

#### Planned
DBMS MonetDB-BHT-8 - Pods [[1, 1, 5, 5]]

### Execution - SUT
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1    21745.36    17.29        173.03               283.57
MonetDB-BHT-8-2    18120.57    20.21        188.28               290.39
MonetDB-BHT-8-3    43989.47    42.21        461.98               484.15
MonetDB-BHT-8-4    50356.12    45.19        457.93               484.00

### Execution - Benchmarker
                 CPU [CPUs]  Max CPU  Max RAM [Gb]  Max RAM Cached [Gb]
MonetDB-BHT-8-1       39.84     0.10          0.38                 0.41
MonetDB-BHT-8-2       39.84     0.01          0.63                 0.66
MonetDB-BHT-8-3       80.27     0.03          1.58                 1.62
MonetDB-BHT-8-4      126.49     0.12          1.78                 1.82

### Tests
TEST passed: Geo Times [s] contains no 0 or NaN
TEST passed: Power@Size [~Q/h] contains no 0 or NaN
TEST passed: Throughput@Size [~GB/h] contains no 0 or NaN
TEST failed: SQL errors
TEST failed: SQL warnings (result mismatch)
TEST passed: Execution SUT contains no 0 or NaN in CPU [CPUs]
TEST passed: Execution Benchmarker contains no 0 or NaN in CPU [CPUs]
TEST passed: Workflow as planned
