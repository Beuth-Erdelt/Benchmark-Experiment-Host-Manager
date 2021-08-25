# Image of TPC-DS Data

This image contains [TPC-H](http://www.tpc.org/tpcds/) data at SF=1.
Data will be copied to `/data/tpcds/SF1`.
This directory is supposed to be mounted to a volume or persistent volume in a shared filesystem.

## Build Commands

```
docker build -t perdelt/bexhoma:data-tpcds-1 --no-cache .
docker push perdelt/bexhoma:data-tpcds-1
```
