# Generator for YCSB data

The image is based on https://github.com/brianfrankcooper/YCSB

The following parameter (ENV) have been added:

* `SF`: Scaling factor. Number of rows = 100000xSF, if not set otherwise. Number of operations = 100000xSF, if not set otherwise. 
* `BEXHOMA_NUM_PODS`: Number of parallel pods
* `BEXHOMA_CHILD`: Number of the current pod. This will be overwritten by entry in Redis queue.
* `BEXHOMA_RNGSEED`: Random Seed. Currently ignored.
* `BEXHOMA_DBMS`: Type of dbms to connect do (jdbc, redis)
* `BEXHOMA_URL`: For db.url
* `BEXHOMA_HOST`: Ignored for JDBC, host info for Redis.
* `BEXHOMA_PORT`: Ignored for JDBC, port info for Redis.
* `BEXHOMA_JAR`: Name of JDBC jar file to be included into YCSB. See Dockerfile for jars included.
* `BEXHOMA_DRIVER`: For db.driver
* `BEXHOMA_CONNECTION`: Name of the Bexhoma connection. Used for connecting to Redis queue.
* `BEXHOMA_EXPERIMENT`: Id of the Bexhoma experiment. Used for connecting to Redis queue.
* `BEXHOMA_EXPERIMENT_RUN`: number of total runs (for repetition of the complete experiment)
* `BEXHOMA_USER`: For db.user
* `BEXHOMA_PASSWORD`: For db.passwd
* `BEXHOMA_DATABASE`: Ignored
* `BEXHOMA_TIME_START`: Optional. If non-zero, pod will wait until time encoded in this var before starting doing something.
* `BEXHOMA_TIME_NOW`: Optional. Includes time about planned start.
* `YCSB_THREADCOUNT`: YCSB workload property threadcount
* `YCSB_TARGET`: YCSB workload property target
* `YCSB_STATUS_INTERVAL`: YCSB workload property status.interval
* `YCSB_STATUS`: If non-zero, YCSB is called with `-s` (report status)
* `YCSB_WORKLOAD`: YCSB workload name (a,b,c,d,e,f)
* `YCSB_BATCHSIZE`: YCSB workload property db.batchsize
* `YCSB_ROWS`: Number of rows
* `YCSB_OPERATIONS`: Number of operations
* `YCSB_MEASUREMENT_TYPE`: YCSB workload property measurementtype. (hdrhistogram, default is histogram)


This folder contains the Dockerfile for a data generator, that loads data into a DBMS.
