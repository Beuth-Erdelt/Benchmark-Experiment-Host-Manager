# TPC-H Refresh Generator

Generates TPC-H RF1/RF2 update files using `dbgen -U N` and stores them on the
persistent data volume at `/data/tpch-refresh/SF<SF>/`.

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
