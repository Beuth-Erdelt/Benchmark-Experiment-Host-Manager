# Generator for TPC-H data

The image is based on https://www.tpc.org/tpch/

The following parameter (ENV) have been added:

* `SF`: 
* `BEXHOMA_NUM_PODS`: 
* `BEXHOMA_CHILD`: 
* `RNGSEED`: 
* `CONNECTION`: 
* `EXPERIMENT`: 
* `STORE_RAW_DATA`: 
* `STORE_RAW_DATA_RECREATE`: 
* `TRANSFORM_RAW_DATA`: 
* `BEXHOMA_SYNCH_GENERATE`: 

This folder contains the Dockerfile for a data generator, that generates data to (RAM) disk.

The Dockerfile expects `dbgen` and `dists.dss` in the current directory.
