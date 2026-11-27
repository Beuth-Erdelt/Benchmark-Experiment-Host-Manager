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

# At most this many docker builds and this many docker pushes run at the
# same time. The two limits are independent.
_MAX_PARALLEL_BUILDS=10
_MAX_PARALLEL_PUSHES=10
_BUILD_SLOTS="$_LOGDIR/build_slots"
_PUSH_SLOTS="$_LOGDIR/push_slots"
mkdir -p "$_BUILD_SLOTS" "$_PUSH_SLOTS"

_run_in_slot() {
  # Run a command once one of <max> slots in <slotdir> is free.
  # Usage: _run_in_slot <slotdir> <max> <command> [args...]
  # A slot is a lock file held with flock across the background subshells.
  # The kernel releases the lock when the fd is closed or the job dies.
  # (mkdir as a lock is not reliable: two jobs could get the same slot.)
  # Returns the exit code of the command.
  local slotdir="$1" max="$2" slot fd rc
  shift 2
  while true; do
    for ((slot = 1; slot <= max; slot++)); do
      exec {fd}>"$slotdir/$slot.lock"
      if flock -n "$fd"; then
        # {fd}>&- keeps the lock fd out of the command's processes;
        # && / || keep set -e from exiting before the slot is released
        "$@" {fd}>&- && rc=0 || rc=$?
        exec {fd}>&-
        return $rc
      fi
      exec {fd}>&-
    done
    sleep 2
  done
}

_build_slot() {
  # Run a command that builds an image, limited to _MAX_PARALLEL_BUILDS.
  # Usage: _build_slot <command> [args...]
  _run_in_slot "$_BUILD_SLOTS" "$_MAX_PARALLEL_BUILDS" "$@"
}

_build() {
  # docker build, limited to _MAX_PARALLEL_BUILDS concurrent builds.
  # Usage: _build <docker build args...>
  _build_slot docker build "$@"
}

_push() {
  # docker push, limited to _MAX_PARALLEL_PUSHES concurrent pushes.
  # Usage: _push <image:tag>
  _run_in_slot "$_PUSH_SLOTS" "$_MAX_PARALLEL_PUSHES" docker push "$1"
}

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
    _build_slot python create_Dockerfiles.py --version "$dbmsbenchmarker" --image-tag "$version"
    _push "bexhoma/evaluator_dbmsbenchmarker:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/evaluator_dbmsbenchmarker:$version"

  (
    set -e
    cd images/benchmarker_dbmsbenchmarker
    _build_slot python create_Dockerfiles.py --version "$dbmsbenchmarker" --image-tag "$version"
    _push "bexhoma/benchmarker_dbmsbenchmarker:$version"
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
    _build -f Dockerfile -t "bexhoma/generator_tpcds:$version" .
    _push "bexhoma/generator_tpcds:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_tpcds:$version"

  (
    set -e
    cd images/tpcds/loader_postgresql
    _build -f Dockerfile -t "bexhoma/loader_tpcds_postgresql:$version" .
    _push "bexhoma/loader_tpcds_postgresql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_postgresql:$version"

  (
    set -e
    cd images/tpcds/loader_db2
    _build -f Dockerfile -t "bexhoma/loader_tpcds_db2:$version" .
    _push "bexhoma/loader_tpcds_db2:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_db2:$version"

  (
    set -e
    cd images/tpcds/loader_mysql
    _build -f Dockerfile -t "bexhoma/loader_tpcds_mysql:$version" .
    _push "bexhoma/loader_tpcds_mysql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_mysql:$version"

  (
    set -e
    cd images/tpcds/loader_mariadb
    _build -f Dockerfile -t "bexhoma/loader_tpcds_mariadb:$version" .
    _push "bexhoma/loader_tpcds_mariadb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_mariadb:$version"

  (
    set -e
    cd images/tpcds/loader_monetdb
    _build -f Dockerfile -t "bexhoma/loader_tpcds_monetdb:$version" .
    _push "bexhoma/loader_tpcds_monetdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_monetdb:$version"

  (
    set -e
    cd images/tpcds/loader_clickhouse
    _build -f Dockerfile -t "bexhoma/loader_tpcds_clickhouse:$version" .
    _push "bexhoma/loader_tpcds_clickhouse:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpcds_clickhouse:$version"
}

###########
build_and_push_ssb() {
  local version="$1"

  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_ssb <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/ssb/generator
    _build -f Dockerfile -t "bexhoma/generator_ssb:$version" .
    _push "bexhoma/generator_ssb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_ssb:$version"

  (
    set -e
    cd images/ssb/loader_postgresql
    _build -f Dockerfile -t "bexhoma/loader_ssb_postgresql:$version" .
    _push "bexhoma/loader_ssb_postgresql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_ssb_postgresql:$version"

  (
    set -e
    cd images/ssb/loader_monetdb
    _build -f Dockerfile -t "bexhoma/loader_ssb_monetdb:$version" .
    _push "bexhoma/loader_ssb_monetdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_ssb_monetdb:$version"

  (
    set -e
    cd images/ssb/loader_clickhouse
    _build -f Dockerfile -t "bexhoma/loader_ssb_clickhouse:$version" .
    _push "bexhoma/loader_ssb_clickhouse:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_ssb_clickhouse:$version"

  (
    set -e
    cd images/ssb/loader_mysql
    _build -f Dockerfile -t "bexhoma/loader_ssb_mysql:$version" .
    _push "bexhoma/loader_ssb_mysql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_ssb_mysql:$version"

  (
    set -e
    cd images/ssb/loader_mariadb
    _build -f Dockerfile -t "bexhoma/loader_ssb_mariadb:$version" .
    _push "bexhoma/loader_ssb_mariadb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_ssb_mariadb:$version"
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
    _build -f Dockerfile -t "bexhoma/generator_tpch:$version" .
    _push "bexhoma/generator_tpch:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_tpch:$version"

  (
    set -e
    cd images/tpch/loader_postgresql
    _build -f Dockerfile -t "bexhoma/loader_tpch_postgresql:$version" .
    _push "bexhoma/loader_tpch_postgresql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_postgresql:$version"

  (
    set -e
    cd images/tpch/loader_mysql
    _build -f Dockerfile -t "bexhoma/loader_tpch_mysql:$version" .
    _push "bexhoma/loader_tpch_mysql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_mysql:$version"

  (
    set -e
    cd images/tpch/loader_mariadb
    _build -f Dockerfile -t "bexhoma/loader_tpch_mariadb:$version" .
    _push "bexhoma/loader_tpch_mariadb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_mariadb:$version"

  (
    set -e
    cd images/tpch/loader_monetdb
    _build -f Dockerfile -t "bexhoma/loader_tpch_monetdb:$version" .
    _push "bexhoma/loader_tpch_monetdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_monetdb:$version"

  (
    set -e
    cd images/tpch/loader_clickhouse
    _build -f Dockerfile -t "bexhoma/loader_tpch_clickhouse:$version" .
    _push "bexhoma/loader_tpch_clickhouse:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_clickhouse:$version"

  (
    set -e
    cd images/tpch/loader_sqlserver
    _build -f Dockerfile -t "bexhoma/loader_tpch_sqlserver:$version" .
    _push "bexhoma/loader_tpch_sqlserver:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_sqlserver:$version"

  (
    set -e
    cd images/tpch/loader_oracle
    _build -f Dockerfile -t "bexhoma/loader_tpch_oracle:$version" .
    _push "bexhoma/loader_tpch_oracle:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_oracle:$version"

  (
    set -e
    cd images/tpch/loader_db2
    _build -f Dockerfile -t "bexhoma/loader_tpch_db2:$version" .
    _push "bexhoma/loader_tpch_db2:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_db2:$version"
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
    _build -f Dockerfile -t "bexhoma/monitoring:$version" .
    _push "bexhoma/monitoring:$version"
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
    _build -f Dockerfile -t "bexhoma/benchmarker_hammerdb:$version" .
    _push "bexhoma/benchmarker_hammerdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/benchmarker_hammerdb:$version"

  (
    set -e
    cd images/hammerdb/generator
    _build -f Dockerfile -t "bexhoma/generator_hammerdb:$version" .
    _push "bexhoma/generator_hammerdb:$version"
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
    _build -f Dockerfile -t "bexhoma/benchmarker_ycsb:$version" .
    _push "bexhoma/benchmarker_ycsb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/benchmarker_ycsb:$version"

  (
    set -e
    cd images/ycsb/generator
    _build -f Dockerfile -t "bexhoma/generator_ycsb:$version" .
    _push "bexhoma/generator_ycsb:$version"
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
    _build -f Dockerfile -t "bexhoma/generator_tpch_refresh:$version" .
    _push "bexhoma/generator_tpch_refresh:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_tpch_refresh:$version"

  (
    set -e
    cd images/tpch_refresh/loader_postgresql
    _build -f Dockerfile -t "bexhoma/loader_tpch_refresh_postgresql:$version" .
    _push "bexhoma/loader_tpch_refresh_postgresql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_postgresql:$version"

  (
    set -e
    cd images/tpch_refresh/loader_mysql
    _build -f Dockerfile -t "bexhoma/loader_tpch_refresh_mysql:$version" .
    _push "bexhoma/loader_tpch_refresh_mysql:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_mysql:$version"

  (
    set -e
    cd images/tpch_refresh/loader_mariadb
    _build -f Dockerfile -t "bexhoma/loader_tpch_refresh_mariadb:$version" .
    _push "bexhoma/loader_tpch_refresh_mariadb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_mariadb:$version"

  (
    set -e
    cd images/tpch_refresh/loader_monetdb
    _build -f Dockerfile -t "bexhoma/loader_tpch_refresh_monetdb:$version" .
    _push "bexhoma/loader_tpch_refresh_monetdb:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_monetdb:$version"
  (
    set -e
    cd images/tpch_refresh/loader_clickhouse
    _build -f Dockerfile -t "bexhoma/loader_tpch_refresh_clickhouse:$version" .
    _push "bexhoma/loader_tpch_refresh_clickhouse:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_clickhouse:$version"

  (
    set -e
    cd images/tpch_refresh/loader_sqlserver
    _build -f Dockerfile -t "bexhoma/loader_tpch_refresh_sqlserver:$version" .
    _push "bexhoma/loader_tpch_refresh_sqlserver:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_sqlserver:$version"

  (
    set -e
    cd images/tpch_refresh/loader_oracle
    _build -f Dockerfile -t "bexhoma/loader_tpch_refresh_oracle:$version" .
    _push "bexhoma/loader_tpch_refresh_oracle:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_oracle:$version"

  (
    set -e
    cd images/tpch_refresh/loader_db2
    _build -f Dockerfile -t "bexhoma/loader_tpch_refresh_db2:$version" .
    _push "bexhoma/loader_tpch_refresh_db2:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/loader_tpch_refresh_db2:$version"
}

###########
build_and_push_hardware() {
  local version="$1"
  if [[ -z "$version" ]]; then
    echo "Usage: build_and_push_hardware <image_tag>"
    return 1
  fi

  (
    set -e
    cd images/hardware/benchmarker
    _build -f Dockerfile -t "bexhoma/benchmarker_hardware:$version" .
    _push "bexhoma/benchmarker_hardware:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/benchmarker_hardware:$version"

  (
    set -e
    cd images/hardware/sut
    _build -f Dockerfile -t "bexhoma/sut_hardware:$version" .
    _push "bexhoma/sut_hardware:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/sut_hardware:$version"
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
    _build -f Dockerfile_generator -t "bexhoma/generator_benchbase:$version" .
    _push "bexhoma/generator_benchbase:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/generator_benchbase:$version"

  (
    set -e
    cd images/benchbase
    _build -f Dockerfile_benchmarker -t "bexhoma/benchmarker_benchbase:$version" .
    _push "bexhoma/benchmarker_benchbase:$version"
  ) >"$(_next_log)" 2>&1 &
  _bg "bexhoma/benchmarker_benchbase:$version"
}


#####

_any_failed=0

# The DBMS-Benchmarker images use the installed version (set by requirements.txt);
# its git tags have the form vX.Y.Z.
dbmsbenchmarker="v$(python -m pip show dbmsbenchmarker | awk '/^Version:/ {print $2}')"
if [[ "$dbmsbenchmarker" == "v" ]]; then
  echo "dbmsbenchmarker is not installed" >&2
  exit 1
fi
echo "DBMS-Benchmarker $dbmsbenchmarker"
version=$(python -m pip show bexhoma | awk '/^Version:/ {print $2}')
echo "$version"

build_and_push_dbmsbenchmarker "$dbmsbenchmarker" "$version"
build_and_push_tpch "$version"
build_and_push_tpch_refresh "$version"
build_and_push_tpcds "$version"
build_and_push_ssb "$version"
build_and_push_monitoring "$version"
build_and_push_hammerdb "$version"
build_and_push_ycsb "$version"
build_and_push_benchbase "$version"
build_and_push_hardware "$version"

_wait_all || _any_failed=1
echo "All version builds and pushes completed."

version="latest"
echo "$version"

build_and_push_dbmsbenchmarker "$dbmsbenchmarker" "$version"
build_and_push_tpch "$version"
build_and_push_tpch_refresh "$version"
build_and_push_tpcds "$version"
build_and_push_ssb "$version"
build_and_push_monitoring "$version"
build_and_push_hammerdb "$version"
build_and_push_ycsb "$version"
build_and_push_benchbase "$version"
build_and_push_hardware "$version"

_wait_all || _any_failed=1
echo "All latest builds and pushes completed."

exit $_any_failed
