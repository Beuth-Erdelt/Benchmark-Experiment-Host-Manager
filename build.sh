
dbmsbenchmarker="v0.14.16"
version=$(python -m pip show bexhoma | awk '/^Version:/ {print $2}')
version="latest"

echo "$version"

cd images

###########

cd evaluator_dbmsbenchmarker
python create_Dockerfiles.py --version $dbmsbenchmarker --image-tag $version
docker push bexhoma/evaluator_dbmsbenchmarker:$version &
cd ..

cd benchmarker_dbmsbenchmarker
python create_Dockerfiles.py --version $dbmsbenchmarker --image-tag $version
docker push bexhoma/benchmarker_dbmsbenchmarker:$version &
cd ..

###########
cd tpcds
cd generator
docker build -f Dockerfile -t bexhoma/generator_tpcds:$version .
docker push bexhoma/generator_tpcds:$version &
cd ..

cd loader_postgresql
docker build -f Dockerfile -t bexhoma/loader_tpcds_postgresql:$version .
docker push bexhoma/loader_tpcds_postgresql:$version &
cd ..

cd loader_mysql
docker build -f Dockerfile -t bexhoma/loader_tpcds_mysql:$version .
docker push bexhoma/loader_tpcds_mysql:$version &
cd ..

cd loader_mariadb
docker build -f Dockerfile -t bexhoma/loader_tpcds_mariadb:$version .
docker push bexhoma/loader_tpcds_mariadb:$version &
cd ..

cd loader_monetdb
docker build -f Dockerfile -t bexhoma/loader_tpcds_monetdb:$version .
docker push bexhoma/loader_tpcds_monetdb:$version &
cd ..
cd ..


###########
cd tpch
cd generator
docker build -f Dockerfile -t bexhoma/generator_tpch:$version .
docker push bexhoma/generator_tpch:$version &
cd ..

cd loader_postgresql
docker build -f Dockerfile -t bexhoma/loader_tpch_postgresql:$version .
docker push bexhoma/loader_tpch_postgresql:$version &
cd ..

cd loader_mysql
docker build -f Dockerfile -t bexhoma/loader_tpch_mysql:$version .
docker push bexhoma/loader_tpch_mysql:$version &
cd ..

cd loader_mariadb
docker build -f Dockerfile -t bexhoma/loader_tpch_mariadb:$version .
docker push bexhoma/loader_tpch_mariadb:$version &
cd ..

cd loader_monetdb
docker build -f Dockerfile -t bexhoma/loader_tpch_monetdb:$version .
docker push bexhoma/loader_tpch_monetdb:$version &
cd ..
cd ..

###########
cd monitoring
docker build -f Dockerfile -t bexhoma/monitoring:$version .
docker push bexhoma/monitoring:$version &
cd ..

###########
cd hammerdb
cd benchmarker
docker build -f Dockerfile -t bexhoma/benchmarker_hammerdb:$version .
docker push bexhoma/benchmarker_hammerdb:$version &
cd ..
cd generator
docker build -f Dockerfile -t bexhoma/generator_hammerdb:$version .
docker push bexhoma/generator_hammerdb:$version &
cd ..
cd ..

###########
cd ycsb
cd benchmarker
docker build -f Dockerfile -t bexhoma/benchmarker_ycsb:$version .
docker push bexhoma/benchmarker_ycsb:$version &
cd ..
cd generator
docker build -f Dockerfile -t bexhoma/generator_ycsb:$version .
docker push bexhoma/generator_ycsb:$version &
cd ..
cd ..

###########
cd benchbase
docker build -t bexhoma/generator_benchbase:$version -f Dockerfile_generator  .
docker push bexhoma/generator_benchbase:$version &
docker build -t bexhoma/benchmarker_benchbase:$version -f Dockerfile_benchmarker  .
docker push bexhoma/benchmarker_benchbase:$version &
cd ..

cd ..
