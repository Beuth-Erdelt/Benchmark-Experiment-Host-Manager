#!/bin/bash

cd images

###########

cd evaluator_dbmsbenchmarker
python create_Dockerfiles.py
#docker build -f Dockerfile_v0.13.6 -t bexhoma/evaluator_dbmsbenchmarker:v0.13.6 --no-cache .
docker push bexhoma/evaluator_dbmsbenchmarker:v0.14.11 &
cd ..

cd benchmarker_dbmsbenchmarker
python create_Dockerfiles.py
#docker build -f Dockerfile_v0.13.6 -t bexhoma/benchmarker_dbmsbenchmarker:v0.13.6 --no-cache .
docker push bexhoma/benchmarker_dbmsbenchmarker:v0.14.11 &
cd ..

###########
cd tpcds
cd generator
docker build -f Dockerfile -t bexhoma/generator_tpcds:latest .
docker push bexhoma/generator_tpcds:latest &
cd ..

cd loader_postgresql
docker build -f Dockerfile -t bexhoma/loader_tpcds_postgresql:latest .
docker push bexhoma/loader_tpcds_postgresql:latest &
cd ..

cd loader_mysql
docker build -f Dockerfile -t bexhoma/loader_tpcds_mysql:latest .
docker push bexhoma/loader_tpcds_mysql:latest &
cd ..

cd loader_mariadb
docker build -f Dockerfile -t bexhoma/loader_tpcds_mariadb:latest .
docker push bexhoma/loader_tpcds_mariadb:latest &
cd ..

cd loader_monetdb
docker build -f Dockerfile -t bexhoma/loader_tpcds_monetdb:latest .
docker push bexhoma/loader_tpcds_monetdb:latest &
cd ..
cd ..


###########
cd tpch
cd generator
docker build -f Dockerfile -t bexhoma/generator_tpch:latest .
docker push bexhoma/generator_tpch:latest &
cd ..

cd loader_postgresql
docker build -f Dockerfile -t bexhoma/loader_tpch_postgresql:latest .
docker push bexhoma/loader_tpch_postgresql:latest &
cd ..

cd loader_mysql
docker build -f Dockerfile -t bexhoma/loader_tpch_mysql:latest .
docker push bexhoma/loader_tpch_mysql:latest &
cd ..

cd loader_mariadb
docker build -f Dockerfile -t bexhoma/loader_tpch_mariadb:latest .
docker push bexhoma/loader_tpch_mariadb:latest &
cd ..

cd loader_monetdb
docker build -f Dockerfile -t bexhoma/loader_tpch_monetdb:latest .
docker push bexhoma/loader_tpch_monetdb:latest &
cd ..
cd ..

###########
cd monitoring
docker build -f Dockerfile -t bexhoma/monitoring:latest .
docker push bexhoma/monitoring:latest &
cd ..

###########
cd hammerdb
cd benchmarker
docker build -f Dockerfile -t bexhoma/benchmarker_hammerdb:5.0 .
docker push bexhoma/benchmarker_hammerdb:5.0 &
cd ..
cd generator
docker build -f Dockerfile -t bexhoma/generator_hammerdb:5.0 .
docker push bexhoma/generator_hammerdb:5.0 &
cd ..
cd ..

###########
cd ycsb
cd benchmarker
docker build -f Dockerfile -t bexhoma/benchmarker_ycsb:0.17.0 .
docker push bexhoma/benchmarker_ycsb:0.17.0 &
cd ..
cd generator
docker build -f Dockerfile -t bexhoma/generator_ycsb:0.17.0 .
docker push bexhoma/generator_ycsb:0.17.0 &
cd ..
cd ..

###########
cd benchbase
docker build -t bexhoma/generator_benchbase:latest -f Dockerfile_generator .
docker push bexhoma/generator_benchbase:latest
docker build -t bexhoma/benchmarker_benchbase:latest -f Dockerfile_benchmarker .
docker push bexhoma/benchmarker_benchbase:latest
cd ..

cd ..
