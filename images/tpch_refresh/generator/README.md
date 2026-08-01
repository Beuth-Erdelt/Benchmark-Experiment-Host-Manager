# TPC-H Refresh Generator

Generates TPC-H RF1/RF2 update files using `dbgen -U N` and stores them on the
persistent data volume at `/data/tpch-refresh/SF<SF>/`.

See [../README.md](../README.md) for the shared refresh-stream pipeline design.

## Execution flow (`generator.sh`)

1. Compute `LAST_SET = TPCH_REFRESH_STREAM_OFFSET + TPCH_REFRESH_STREAMS`.
2. Determine `destination_raw`: `/data/tpch-refresh/SF<SF>/` if `STORE_RAW_DATA=1`,
   else `/tmp/tpch-refresh/SF<SF>/`.
3. **Fast exit** if `delete.$LAST_SET` already exists — emits timing and exits 0.
4. Copy `dbgen` and `dists.dss` into `destination_raw`, run
   `./dbgen -s SF -U LAST_SET`, then remove the executables.
   Existing sets (lower K) are overwritten with identical deterministic content —
   harmless because `dbgen` output is fully determined by SF and set number.
5. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END`.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `SF` | `1` | TPC-H scaling factor |
| `TPCH_REFRESH_STREAMS` | `1` | Number of RF1+RF2 pairs to generate per run |
| `TPCH_REFRESH_STREAM_OFFSET` | `0` | Generate sets `OFFSET+1` through `OFFSET+STREAMS` |
| `STORE_RAW_DATA` | `1` | `1` = persist to `/data/tpch-refresh/SF<SF>/`; `0` = use `/tmp/tpch-refresh/SF<SF>/` |
| `BEXHOMA_CONNECTION` | `postgresql` | Connection name (used in Redis counter keys) |
| `BEXHOMA_EXPERIMENT` | `12345` | Experiment identifier |

## Generated files

`dbgen -s SF -U N` produces in `$destination_raw`:

```
orders.tbl.u1  lineitem.tbl.u1  delete.1
orders.tbl.u2  lineitem.tbl.u2  delete.2
...
orders.tbl.uN  lineitem.tbl.uN  delete.N
```

where `N = TPCH_REFRESH_STREAM_OFFSET + TPCH_REFRESH_STREAMS`.

## Build note

`dbgen` and `dists.dss` must be copied from `images/tpch/generator/` into this
directory before building the image.
