# Generator for TPC-DS data

The image is based on https://www.tpc.org/tpcds/

The following parameter (ENV) have been added:

* `SF`: 
* `NUM_PODS`: 
* `CHILD`: 
* `RNGSEED`: 
* `CONNECTION`: 
* `EXPERIMENT`: 
* `STORE_RAW_DATA`: 
* `STORE_RAW_DATA_RECREATE`: 
* `TRANSFORM_RAW_DATA`: 
* `BEXHOMA_SYNCH_GENERATE`: 

This folder contains the Dockerfile for a data generator, that generates data to (RAM) disk.

The Dockerfile expects `dsdgen` and `tpcds.idx` in the current directory.
