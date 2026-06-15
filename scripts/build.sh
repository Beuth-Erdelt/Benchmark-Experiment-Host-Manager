#!/bin/bash
# Library of functions for building and pushing bexhoma Docker images.
#
# Defines build_and_push_* helpers that build images for the evaluator and
# benchmarker components and push them to the bexhoma Docker Hub repository.
# All background jobs are tracked; failures are logged and reported at the end.
# Intended to be called directly from the project root.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

#### Error tracking ####

_LOGDIR=$(mktemp -d)
_PIDS=()
_LABELS=()
_LOGFILES=()

trap 'rm -rf "$_LOGDIR"' EXIT

_next_log() {
  # Return the log file path for the next job to be registered.
  # Evaluated before the background process is launched, so ${#_PIDS[@]}
  # gives the correct next index.
  echo "$_LOGDIR/${#_PIDS[@]}.log"
}

_bg() {
  # Register the most recently backgrounded process.
  # Usage: _bg <label>
  # Must be called immediately after the trailing &.
  local label="$1"
  local logfile="$_LOGDIR/${#_PIDS[@]}.log"
  _PIDS+=($!)
  _LABELS+=("$label")
  _LOGFILES+=("$logfile")
}

_wait_all() {
  # Wait for all registered background jobs.
  # Prints each failed job's log to stderr, then a summary of all failures.
  # Returns 1 if any job failed, 0 otherwise.
  local errors=()
  for i in "${!_PIDS[@]}"; do
    local pid="${_PIDS[$i]}"
    local label="${_LABELS[$i]}"
    local logfile="${_LOGFILES[$i]}"
    wait "$pid"
    local rc=$?
    if [[ $rc -ne 0 ]]; then
      errors+=("$label")
      echo "" >&2
      echo "=== ERROR: $label (exit $rc) ===" >&2
      cat "$logfile" >&2
    fi
  done
  _PIDS=()
  _LABELS=()
  _LOGFILES=()
  if [[ ${#errors[@]} -gt 0 ]]; then
    echo "" >&2
    echo "=== FAILED BUILDS ===" >&2
    for e in "${errors[@]}"; do
      echo "  FAILED: $e" >&2
    done
    return 1
  fi
}


###########
build_and_push_dbmsbenchmarker() {
  local dbmsbenchmarker="$1"
  local version="$2"

  if [[ -z "$dbmsbenchmarker" || -z "$version" ]]; then
    echo "Usage: build_and_push_dbmsbenchmarker <dbmsbenchmarker_version> <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/evaluator_dbmsbenchmarker
    python create_Dockerfiles.py --version "$dbmsbenchmarker" --image-tag "$version"
    docker push "bexhoma/evaluator_dbmsbenchmarker:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/evaluator_dbmsbenchmarker:$version"

  (
    set -e
    cd images/benchmarker_dbmsbenchmarker
    python create_Dockerfiles.py --version "$dbmsbenchmarker" --image-tag "$version"
    docker push "bexhoma/benchmarker_dbmsbenchmarker:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/benchmarker_dbmsbenchmarker:$version"
}


###########
build_and_push_tpcds() {
  local version="$1"

  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_tpcds <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/tpcds/generator
    docker build -f Dockerfile -t "bexhoma/generator_tpcds:$version" .
    docker push "bexhoma/generator_tpcds:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_tpcds:$version"

  (
    set -e
    cd images/tpcds/loader_postgresql
    docker build -f Dockerfile -t "bexhoma/loader_tpcds_postgresql:$version" .
    docker push "bexhoma/loader_tpcds_postgresql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_postgresql:$version"

  (
    set -e
    cd images/tpcds/loader_mysql
    docker build -f Dockerfile -t "bexhoma/loader_tpcds_mysql:$version" .
    docker push "bexhoma/loader_tpcds_mysql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_mysql:$version"

  (
    set -e
    cd images/tpcds/loader_mariadb
    docker build -f Dockerfile -t "bexhoma/loader_tpcds_mariadb:$version" .
    docker push "bexhoma/loader_tpcds_mariadb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_mariadb:$version"

  (
    set -e
    cd images/tpcds/loader_monetdb
    docker build -f Dockerfile -t "bexhoma/loader_tpcds_monetdb:$version" .
    docker push "bexhoma/loader_tpcds_monetdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_monetdb:$version"
}


###########
build_and_push_tpch() {
  local version="$1"

  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_tpch <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/tpch/generator
    docker build -f Dockerfile -t "bexhoma/generator_tpch:$version" .
    docker push "bexhoma/generator_tpch:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_tpch:$version"

  (
    set -e
    cd images/tpch/loader_postgresql
    docker build -f Dockerfile -t "bexhoma/loader_tpch_postgresql:$version" .
    docker push "bexhoma/loader_tpch_postgresql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_postgresql:$version"

  (
    set -e
    cd images/tpch/loader_mysql
    docker build -f Dockerfile -t "bexhoma/loader_tpch_mysql:$version" .
    docker push "bexhoma/loader_tpch_mysql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_mysql:$version"

  (
    set -e
    cd images/tpch/loader_mariadb
    docker build -f Dockerfile -t "bexhoma/loader_tpch_mariadb:$version" .
    docker push "bexhoma/loader_tpch_mariadb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_mariadb:$version"

  (
    set -e
    cd images/tpch/loader_monetdb
    docker build -f Dockerfile -t "bexhoma/loader_tpch_monetdb:$version" .
    docker push "bexhoma/loader_tpch_monetdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_monetdb:$version"
}


###########
build_and_push_monitoring() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_monitoring <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/monitoring
    docker build -f Dockerfile -t "bexhoma/monitoring:$version" .
    docker push "bexhoma/monitoring:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/monitoring:$version"
}

###########
build_and_push_hammerdb() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_hammerdb <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/hammerdb/benchmarker
    docker build -f Dockerfile -t "bexhoma/benchmarker_hammerdb:$version" .
    docker push "bexhoma/benchmarker_hammerdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/benchmarker_hammerdb:$version"

  (
    set -e
    cd images/hammerdb/generator
    docker build -f Dockerfile -t "bexhoma/generator_hammerdb:$version" .
    docker push "bexhoma/generator_hammerdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_hammerdb:$version"
}

###########
build_and_push_ycsb() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_ycsb <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/ycsb/benchmarker
    docker build -f Dockerfile -t "bexhoma/benchmarker_ycsb:$version" .
    docker push "bexhoma/benchmarker_ycsb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/benchmarker_ycsb:$version"

  (
    set -e
    cd images/ycsb/generator
    docker build -f Dockerfile -t "bexhoma/generator_ycsb:$version" .
    docker push "bexhoma/generator_ycsb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_ycsb:$version"
}

###########
build_and_push_tpch_refresh() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_tpch_refresh <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/tpch_refresh/generator
    docker build -f Dockerfile -t "bexhoma/generator_tpch_refresh:$version" .
    docker push "bexhoma/generator_tpch_refresh:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_tpch_refresh:$version"

  (
    set -e
    cd images/tpch_refresh/loader_postgresql
    docker build -f Dockerfile -t "bexhoma/loader_tpch_refresh_postgresql:$version" .
    docker push "bexhoma/loader_tpch_refresh_postgresql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_postgresql:$version"

  (
    set -e
    cd images/tpch_refresh/loader_mysql
    docker build -f Dockerfile -t "bexhoma/loader_tpch_refresh_mysql:$version" .
    docker push "bexhoma/loader_tpch_refresh_mysql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_mysql:$version"
}

###########
build_and_push_benchbase() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_benchbase <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/benchbase
    docker build -f Dockerfile_generator -t "bexhoma/generator_benchbase:$version" .
    docker push "bexhoma/generator_benchbase:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_benchbase:$version"

  (
    set -e
    cd images/benchbase
    docker build -f Dockerfile_benchmarker -t "bexhoma/benchmarker_benchbase:$version" .
    docker push "bexhoma/benchmarker_benchbase:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/benchmarker_benchbase:$version"
}


#####

_any_failed=0

dbmsbenchmarker="v0.14.20"
version=$(python -m pip show bexhoma | awk '/^Version:/ {print $2}')
echo "$version"

build_and_push_dbmsbenchmarker "$dbmsbenchmarker" "$version"
build_and_push_tpch "$version"
build_and_push_tpch_refresh "$version"
build_and_push_tpcds "$version"
build_and_push_monitoring "$version"
build_and_push_hammerdb "$version"
build_and_push_ycsb "$version"
build_and_push_benchbase "$version"

_wait_all || _any_failed=1
echo "All version builds and pushes completed."

version="latest"
echo "$version"

build_and_push_dbmsbenchmarker "$dbmsbenchmarker" "$version"
build_and_push_tpch "$version"
build_and_push_tpch_refresh "$version"
build_and_push_tpcds "$version"
build_and_push_monitoring "$version"
build_and_push_hammerdb "$version"
build_and_push_ycsb "$version"
build_and_push_benchbase "$version"

_wait_all || _any_failed=1
echo "All latest builds and pushes completed."

exit $_any_failed
