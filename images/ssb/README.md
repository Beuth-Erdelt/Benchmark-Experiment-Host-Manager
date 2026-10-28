# SSB images

Images for the Star Schema Benchmark (SSB, O'Neil et al., revision 3, 2009). Two-phase
pipeline as for TPC-H: a generator (initContainer) writes flat files to disk, then the
loader of the same pod reads them and inserts them into the target DBMS.

## Directory layout

```
images/ssb/
├── generator/
│   ├── Dockerfile               — builds dbgen (eyalroz/ssb-dbgen, pinned commit) + runtime image
│   ├── dbgen-chunk-seeds.patch  — fix for chunked lineorder generation (see below)
│   ├── generator.sh             — generates .tbl files; with SSB_SCHEMA_VARIANT=flat also lineorder_flat.tbl
│   ├── flat.awk                 — second half of the flat pipeline (supplier and part lookup)
│   ├── tpc_eula.txt             — TPC license of the dbgen code base
│   └── README.md
├── loader_postgresql/           — psql \COPY
├── loader_monetdb/              — mclient COPY ... FROM STDIN
├── loader_clickhouse/           — clickhouse-client INSERT ... FORMAT CSV (also ClickHouseCluster)
├── loader_mysql/                — LOAD DATA LOCAL INFILE, MySQL client
├── loader_mariadb/              — LOAD DATA LOCAL INFILE, MariaDB client (same loader.sh)
└── README.md                    — this file
```

## Data layout

| Variant | Folder | Files |
|---|---|---|
| normal (`-xsv normal`) | `/data/ssb/SF<SF>[/<N>/<child>]` | `lineorder.tbl[.<child>]`; child 1 also `customer.tbl`, `supplier.tbl`, `part.tbl`, `date.tbl` |
| flat (`-xsv flat`) | `/data/ssb/SF<SF>/flat[/<N>/<child>]` | `lineorder_flat.tbl` |

`<N>` is the number of loader pods; with one pod the files are directly in the SF folder.
Each folder gets a `.complete` marker as the last step of the generator. A folder with the
marker is reused by later experiments; a folder without it (a generator that died halfway)
is generated again. `STORE_RAW_DATA=0` writes to `/tmp/ssb` (in memory) instead of `/data`.

The generator pods of all DBMS configurations of an experiment run at the same time and may
generate the same folder. Each generates into its own `.staging-<pod>` subfolder and moves
the finished files in (atomic rename), then writes `.complete`; a pod that finds the folder
completed meanwhile discards its copy. The generator barrier (`BEXHOMA_SYNCH_GENERATE`) comes
before the check for existing data, so pods that find their folder complete still check in.

## Key design decisions

| Decision | Reason |
|---|---|
| dbgen built from source at a pinned commit | Reproducible, no binary in git. eyalroz/ssb-dbgen merges the fixes of the older SSB dbgen forks. |
| Built with `EOL_HANDLING=ON` | No trailing `\|`, so no `sed` pass and no dummy column |
| Only lineorder is chunked (`-T l -C N -S k`) | In dbgen's chunked path part is scaled linearly (200,000 x SF instead of 200,000 x floor(1+log2 SF)) and date gets 2,557 x SF/N rows. The dimensions are generated unchunked. |
| `dbgen-chunk-seeds.patch` | Unpatched, every chunk after the first restarts the random streams of `lo_custkey` and `lo_orderpriority`, so the data depended on the number of pods. With the patch the chunks are exactly the unchunked `lineorder` (checked at SF1 with 4 chunks and SF10 with 8 chunks). |
| Dimensions only in child 1's folder | Each loader loads its own folder; no "child 1 only" rule in the loaders |
| Table `dates` | `date` is a reserved word; the loaders map `date.tbl` to `dates` |
| Flat files built in the generator | `lineorder_flat` is ingested like any table, in parallel per pod; no join SQL per DBMS |
| Flat join by streaming (`sort`/`join`/`gawk`) | Bounded memory: customer (30,000 x SF rows) by sort-merge, supplier and part (at most about 2 M rows each) as awk lookup tables |

## Flat generation (generator.sh)

1. lineorder chunk: reused from the normal folder if it is complete, otherwise generated.
2. customer, supplier, part: generated in full (dbgen is deterministic, every pod gets the same rows).
3. `sort -k3 lineorder | join customer | gawk -f flat.awk supplier part` writes the 17 lineorder
   columns (dates as `YYYY-MM-DD`), then all customer, supplier and part columns without their keys.
4. `sort -k1n -k2n` restores the lineorder order (`SSB_FLAT_RESTORE_ORDER=1`, default).
5. Row count of the flat file must equal the chunk's row count (`join` drops unmatched rows silently).

Work files (sort temp, dimensions, chunk) go to `SSB_WORK_DIR` (default `/work`, a disk
`emptyDir` in the job templates). With the order restore (default) the peak is about 2x the flat
chunk, about 6.7x the lineorder chunk (SF10 in 8 chunks: 4.9 GB per pod); without it about 1x the
lineorder chunk. Measured locally (Docker Desktop): SF10 chunk of 7.5 M rows in 26 s (18 s without
the order restore); awk holds 180 MB for SF10's supplier and part; the flat file is about 3.4x the
lineorder chunk. `compare-flat.sh` compares this with DuckDB (see `dev/plan-ssb.md`, M1b).

The job templates set no ephemeral-storage request for `/work`: a pod that finds its folder
complete uses none, and a request would reserve the disk on every run. The node must have the
free local disk above while a flat file is generated, or the kubelet evicts the pod.

## Per-DBMS loader differences

| DBMS | Tool | Check |
|---|---|---|
| PostgreSQL (also PgDuckDB, Citus) | `psql \COPY <table> FROM '<file>' delimiter '\|' null ''` | answer must be `COPY <lines of the file>` |
| MonetDB | `mclient COPY <lines> RECORDS INTO <table> FROM STDIN USING DELIMITERS '\|'` | `<lines> affected rows`; retries on worker/producer thread errors |
| ClickHouse (also ClickHouseCluster) | `clickhouse-client --format_csv_delimiter='\|' INSERT INTO <table> FORMAT CSV` | exit code |
| MySQL, MariaDB | `mysql --local-infile=1 -e "LOAD DATA LOCAL INFILE '<file>' INTO TABLE ssb.<table> FIELDS TERMINATED BY '\|'; SELECT ROW_COUNT(); COMMIT;"` | the only output line must be the lines of the file; `COMMIT` because MySQL's load durability switches autocommit off |

The MySQL and MariaDB images differ only in the client and base image, as their TPC-H loaders
(MySQL: the job template sets `MYSQL_CLIENT_OPTIONS=--skip-ssl`); `loader.sh` is the same file.
On the multi-node DBMS the loader writes to the coordinator, which sends the rows to the nodes.

A failed table fails the loader pod (exit 1).

Multi-tenancy is not supported yet; `ssb.py` rejects `-mtn`.
