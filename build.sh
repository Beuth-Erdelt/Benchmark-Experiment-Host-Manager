
###########
build_and_push_dbmsbenchmarker() {
  local dbmsbenchmarker="$1"
  local version="$2"

  if [[ -z "$dbmsbenchmarker" || -z "$version" ]]; then
    echo "Usage: build_and_push_dbmsbenchmarker <dbmsbenchmarker_version> <image_tag>"
    return 1
  fi

  (
    cd images/evaluator_dbmsbenchmarker || exit 1
    python create_Dockerfiles.py --version "$dbmsbenchmarker" --image-tag "$version"
    docker push "bexhoma/evaluator_dbmsbenchmarker:$version"
  ) &

  (
    cd images/benchmarker_dbmsbenchmarker || exit 1
    python create_Dockerfiles.py --version "$dbmsbenchmarker" --image-tag "$version"
    docker push "bexhoma/benchmarker_dbmsbenchmarker:$version"
  ) &
}


###########
build_and_push_tpcds() {
  local version="$1"

  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_tpcds <image_tag>"
    return 1
  fi

  (
    cd images/tpcds/generator || exit 1
    docker build -f Dockerfile -t "bexhoma/generator_tpcds:$version" .
    docker push "bexhoma/generator_tpcds:$version"
  ) &

  (
    cd images/tpcds/loader_postgresql || exit 1
    docker build -f Dockerfile -t "bexhoma/loader_tpcds_postgresql:$version" .
    docker push "bexhoma/loader_tpcds_postgresql:$version"
  ) &

  (
    cd images/tpcds/loader_mysql || exit 1
    docker build -f Dockerfile -t "bexhoma/loader_tpcds_mysql:$version" .
    docker push "bexhoma/loader_tpcds_mysql:$version"
  ) &

  (
    cd images/tpcds/loader_mariadb || exit 1
    docker build -f Dockerfile -t "bexhoma/loader_tpcds_mariadb:$version" .
    docker push "bexhoma/loader_tpcds_mariadb:$version"
  ) &

  (
    cd images/tpcds/loader_monetdb || exit 1
    docker build -f Dockerfile -t "bexhoma/loader_tpcds_monetdb:$version" .
    docker push "bexhoma/loader_tpcds_monetdb:$version"
  ) &
}


###########
build_and_push_tpch() {
  local version="$1"

  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_tpch <image_tag>"
    return 1
  fi

  (
    cd images/tpch/generator || exit 1
    docker build -f Dockerfile -t "bexhoma/generator_tpch:$version" .
    docker push "bexhoma/generator_tpch:$version"
  ) &

  (
    cd images/tpch/loader_postgresql || exit 1
    docker build -f Dockerfile -t "bexhoma/loader_tpch_postgresql:$version" .
    docker push "bexhoma/loader_tpch_postgresql:$version"
  ) &

  (
    cd images/tpch/loader_mysql || exit 1
    docker build -f Dockerfile -t "bexhoma/loader_tpch_mysql:$version" .
    docker push "bexhoma/loader_tpch_mysql:$version"
  ) &

  (
    cd images/tpch/loader_mariadb || exit 1
    docker build -f Dockerfile -t "bexhoma/loader_tpch_mariadb:$version" .
    docker push "bexhoma/loader_tpch_mariadb:$version"
  ) &

  (
    cd images/tpch/loader_monetdb || exit 1
    docker build -f Dockerfile -t "bexhoma/loader_tpch_monetdb:$version" .
    docker push "bexhoma/loader_tpch_monetdb:$version"
  ) &
}


###########
build_and_push_monitoring() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_monitoring <image_tag>"
    return 1
  fi

  (
    cd images/monitoring || exit 1
    docker build -f Dockerfile -t "bexhoma/monitoring:$version" .
    docker push "bexhoma/monitoring:$version"
  ) &
}

###########
build_and_push_hammerdb() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_hammerdb <image_tag>"
    return 1
  fi

  (
    cd images/hammerdb/benchmarker || exit 1
    docker build -f Dockerfile -t "bexhoma/benchmarker_hammerdb:$version" .
    docker push "bexhoma/benchmarker_hammerdb:$version"
  ) &

  (
    cd images/hammerdb/generator || exit 1
    docker build -f Dockerfile -t "bexhoma/generator_hammerdb:$version" .
    docker push "bexhoma/generator_hammerdb:$version"
  ) &
}

###########
build_and_push_ycsb() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_ycsb <image_tag>"
    return 1
  fi

  (
    cd images/ycsb/benchmarker || exit 1
    docker build -f Dockerfile -t "bexhoma/benchmarker_ycsb:$version" .
    docker push "bexhoma/benchmarker_ycsb:$version"
  ) &

  (
    cd images/ycsb/generator || exit 1
    docker build -f Dockerfile -t "bexhoma/generator_ycsb:$version" .
    docker push "bexhoma/generator_ycsb:$version"
  ) &
}

###########
build_and_push_benchbase() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_benchbase <image_tag>"
    return 1
  fi

  (
    cd images/benchbase || exit 1
    docker build -f Dockerfile_generator -t "bexhoma/generator_benchbase:$version" .
    docker push "bexhoma/generator_benchbase:$version"
  ) &

  (
    cd images/benchbase || exit 1
    docker build -f Dockerfile_benchmarker -t "bexhoma/benchmarker_benchbase:$version" .
    docker push "bexhoma/benchmarker_benchbase:$version"
  ) &
}




#####

dbmsbenchmarker="v0.14.17"
version=$(python -m pip show bexhoma | awk '/^Version:/ {print $2}')
echo "$version"

build_and_push_dbmsbenchmarker "$dbmsbenchmarker" "$version"
build_and_push_tpch "$version"
build_and_push_tpcds "$version"
build_and_push_monitoring "$version"
build_and_push_hammerdb "$version"
build_and_push_ycsb "$version"
build_and_push_benchbase "$version"

wait
echo "All version builds and pushes completed."

version="latest"
echo "$version"

build_and_push_dbmsbenchmarker "$dbmsbenchmarker" "$version"
build_and_push_tpch "$version"
build_and_push_tpcds "$version"
build_and_push_monitoring "$version"
build_and_push_hammerdb "$version"
build_and_push_ycsb "$version"
build_and_push_benchbase "$version"

# Wait for all background jobs to finish
wait
echo "All latest builds and pushes completed."
