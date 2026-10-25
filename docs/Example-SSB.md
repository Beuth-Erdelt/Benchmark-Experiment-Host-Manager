# Benchmark: SSB

The Star Schema Benchmark (SSB) is a data warehouse benchmark derived from TPC-H: one fact
table `lineorder` (TPC-H's `lineitem` and `orders` combined) and four dimensions `customer`,
`supplier`, `part` and `dates`, queried by 13 queries in four flights. Bexhoma runs it with the
DBMSBenchmarker, like TPC-H and TPC-DS, on PostgreSQL, MonetDB and ClickHouse.

Two options choose what is measured:

| Option | Values | Meaning |
|---|---|---|
| `-xsv` | `normal` (default), `flat` | star schema, or one denormalized table `lineorder_flat` (lineorder joined with customer, supplier and part, as in the ClickHouse and Doris SSB setups) |
| `-xqv` | `spec` (default), `random` | the constants of the specification, or random parameters that keep the filter factor of each query (after Rabl et al., ICPE 2013) |

Sources:

* Specification: P. O'Neil, E. O'Neil, X. Chen, S. Revilak: *Star Schema Benchmark*, Revision 3, 2009, <https://www.cs.umb.edu/~poneil/StarSchemaB.PDF>
* Data generator: [eyalroz/ssb-dbgen](https://github.com/eyalroz/ssb-dbgen), commit `ae1e254`, built in the generator image with one fix for chunked generation
* Random parameters: T. Rabl, M. Poess, H.-A. Jacobsen, P. O'Neil, E. O'Neil: *Variations of the Star Schema Benchmark to Test the Effects of Data Skew on Query Performance*, ICPE 2013
* Flat table: ClickHouse docs, *Star Schema Benchmark*; Apache Doris docs, *SSB*

The queries are listed in [Queries-SSB.md](Queries-SSB.md).

**The results are not official benchmark results. The exact performance depends on a collection of parameters.**

## Perform Benchmark

```bash
bexhoma ssb run -ms 1 -dbms PostgreSQL
```

Generates SSB data at scale factor 1 (lineorder: 6 million rows), loads it into PostgreSQL and
runs the 13 queries with the constants of the specification.

A typical run, as in `scripts/test-docs-ssb.sh`:

```bash
bexhoma ssb \
  -dbms PostgreSQL \
  -sf 1 \
  -xii -xic -xis \
  -nlp 8 \
  -xdt \
  -ms 1 \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -ks no \
  run
```

This
* generates and loads SSB data at scale factor 1 (`-sf`) with 8 loader pods (`-nlp`)
* creates indexes, primary and foreign keys and statistics after loading (`-xii -xic -xis`)
* measures the data transfer volume of each query (`-xdt`)
* runs one DBMS at a time (`-ms`), with a timeout of 1200 s per query (`-t`)
* tests the result for errors and mismatches (`-tr`)
* limits and requests 64 GiB RAM for the SUT (`-lr`, `-rr`), with a 50 GiB volume if storage is used (`-rss`)
* removes the SUT at the end (`-ks no`)

The summary has the same sections as for TPC-H and TPC-DS: workload, connections, loading
times, per-query latencies, Power@Size, Throughput@Size, errors and warnings (result
mismatches across DBMS) and tests.

## Data Generation and Loading

Each loader pod runs the generator as an init container, then the loader of its DBMS.

* lineorder is generated in as many chunks as there are loader pods (`dbgen -T l -C <N> -S <k>`); pod 1 also generates the dimensions.
* The files are written to the shared volume `bexhoma-data`, `/data/ssb/SF<SF>/<N>/<k>`, and reused by later experiments with the same scale factor and number of pods.
* Each pod loads the files of its own folder, all pods start loading together.
* The chunks are exactly the data of an unchunked generation, so the data does not depend on `-nlp`.

| Table | Rows |
|---|---|
| `customer` | 30,000 x SF |
| `supplier` | 2,000 x SF |
| `part` | 200,000 x floor(1 + log2 SF) |
| `dates` | 2,557 |
| `lineorder` | about 6,000,000 x SF |

Loading tools: `psql \COPY` (PostgreSQL), `mclient COPY` (MonetDB), `clickhouse-client
INSERT ... FORMAT CSV` (ClickHouse). A loader pod fails if a table does not load completely.

`-xlit <table>` loads only one table.

## Flat Table

```bash
bexhoma ssb -dbms PostgreSQL MonetDB ClickHouse -sf 1 -nlp 8 -xsv flat -xii -xis run
```

With `-xsv flat` the generator pods build `lineorder_flat.tbl` from their lineorder chunk and
the full customer, supplier and part tables, before loading. The DBMS then ingests only
`lineorder_flat`, in parallel per pod; the join is not part of the measured loading time.

* Columns: the 17 lineorder columns, then all customer, supplier and part columns without their keys. `lo_orderdate` and `lo_commitdate` are `DATE`.
* The join streams: `sort` and `join` for customer, an awk lookup for supplier and part. Memory stays bounded (a 512 MB sort buffer plus supplier and part, about 1 GB at SF 1000); the sort needs temporary disk space of about 2-3x the chunk on the node.
* The file is about 3.4 times the size of the lineorder data and is stored in `/data/ssb/SF<SF>/flat/<N>/<k>`, next to the star schema files. At SF 100 that is about 200 GB on the shared volume.
* A flat experiment gets its own volume label (`ssb-flat-<SF>`), so it never reuses a volume loaded with the star schema.
* `-xic` has no effect: `lineorder_flat` has no keys to constrain.

The flat queries are the star schema queries with predicates on `lo_orderdate` instead of the
date dimension. They return the same results.

## Random Parameters

```bash
bexhoma ssb -dbms PostgreSQL -sf 1 -nlp 8 -xqv random -xrcp -ne 1,2 run
```

With `-xqv random` each query draws its constants: a year, month, week, region, nation, city,
category or brand from the whole hierarchy level, ranges over discount and quantity with the
width of the specification. Correlated values are drawn together (two cities of one nation, a
nation of the drawn region). So every query keeps the filter factor of the specification.
Without `-xrcp` all streams use the same parameters, with `-xrcp` each stream draws its own.
The drawn values are in the protocol of the experiment.

## Use Persistent Storage

```bash
bexhoma ssb -dbms PostgreSQL -sf 1 -nc 2 -nlp 8 -xii -xic -xis -rsr -rss 50Gi -rst <storage class> run
```

As for TPC-H: the first run loads the data into a persistent volume, the second run (`-nc 2`)
starts the SUT again on that volume and skips loading.

## Reset Scripts

With `-ar` a reset runs before each benchmarking round: `VACUUM ANALYZE`, `CHECKPOINT` and a
statistics reset for PostgreSQL, `ANALYZE` for MonetDB, `sync` for ClickHouse.

## Profiling

```bash
bexhoma ssb -dbms PostgreSQL MonetDB ClickHouse -sf 1 -nlp 8 profiling
```

Runs count, count distinct, minimum and maximum of the key and date columns of each table
instead of the benchmark queries.

## Adjust Parameters

### Command line

| Option | Meaning |
|---|---|
| `-xsv normal\|flat` | schema variant |
| `-xqv spec\|random` | query variant |
| `-xii`, `-xic`, `-xis` | indexes, primary and foreign keys (star schema only), statistics after loading |
| `-xrcp` | with `-xqv random`: new parameters per stream |
| `-xshq` | shuffle the query order per stream |
| `-xaq 1,4,7` | run only these queries (1-based: Q1.1 = 1, Q4.3 = 13) |
| `-xlit <table>` | load only this table |
| `-xdt` | measure the data transfer volume per query |
| `-xve`, `-xse` | print or store EXPLAIN output per query |

Multi-tenancy (`-mtn`) is not supported for SSB yet.

### Files

* Query files and DDL scripts: [`experiments/ssb/`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/experiments/ssb)
* Images (generator and loaders): [`images/ssb/`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/tree/master/images/ssb)
* Job templates: `k8s/jobtemplate-loading-ssb-<DBMS>.yml`
* Script lists: `volumes.ssb` in the cluster config
* Test script with all runs of this page: `scripts/test-docs-ssb.sh` (`.ps1`)
