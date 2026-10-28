######################################################################################
# Dockerfile for Bexhoma - Generator SSB
######################################################################################
#
# This Dockerfile builds an image for a Bexhoma generator for Star Schema Benchmark data.
#
# Base Image: debian:stable-20251103-slim
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2026-10-25
# Version: 1.0
# Description: This container generates SSB .tbl files (pipe-delimited, no trailing
# delimiter) with dbgen from https://github.com/eyalroz/ssb-dbgen, built from a pinned
# commit (plus one seed fix) in the first stage. In multi-pod mode each pod generates one lineorder chunk
# (dbgen -T l -C <num_pods> -S <child>); pod 1 also generates the dimensions. With
# SSB_SCHEMA_VARIANT=flat each pod joins its chunk with customer, supplier and part
# (sort, join, gawk) into lineorder_flat.tbl. The child index is obtained from a
# Redis queue. redis-cli is installed via apt.
######################################################################################

######################################################################################
# Stage 1: build dbgen
######################################################################################
FROM debian:stable-20251103-slim AS build

# eyalroz/ssb-dbgen, commit of 2025-04-27
ARG SSB_DBGEN_COMMIT=ae1e254aa4d603d8ef1f44078e5abed011634b23

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# dbgen-chunk-seeds.patch: in a chunk (-S > 1) dbgen does not advance the random streams
# of lo_custkey, lo_orderpriority (and the unused clerk), so chunked data differed from
# unchunked data; with the patch the chunks are exactly the unchunked lineorder
COPY ./dbgen-chunk-seeds.patch /dbgen-chunk-seeds.patch

RUN git clone https://github.com/eyalroz/ssb-dbgen.git /src \
    && cd /src \
    && git checkout $SSB_DBGEN_COMMIT \
    && git apply /dbgen-chunk-seeds.patch \
    && cmake -B build -DCMAKE_BUILD_TYPE=Release -DEOL_HANDLING=ON \
    && cmake --build build --target dbgen

######################################################################################
# Stage 2: runtime
######################################################################################
FROM debian:stable-20251103-slim

######################################################################################
# Install dependencies
######################################################################################
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        redis-tools \
        gawk \
    && rm -rf /var/lib/apt/lists/*

######################################################################################
# Copy SSB generator files
######################################################################################
COPY ./tpc_eula.txt ./tpc_eula.txt
COPY --from=build /src/build/dbgen /tmp/dbgen
COPY --from=build /src/dists.dss /tmp/dists.dss
RUN chmod +x /tmp/dbgen

COPY ./flat.awk /tmp/flat.awk
COPY ./generator.sh /tmp/generator.sh
RUN chmod +x /tmp/generator.sh

######################################################################################
# Dev only (INCLUDE_DUCKDB=1, tag <version>-duckdb): DuckDB CLI and GNU time for
# compare-flat.sh, which measures the flat generation of generator.sh against DuckDB
######################################################################################
ARG INCLUDE_DUCKDB=0
ARG DUCKDB_VERSION=1.1.3
ARG DUCKDB_SHA256=efd0fccdb1a28d9ec7a6ebfcde59900068b8ba43a846c9b553c0fd2bbe4acf43
COPY ./flat.sql /tmp/flat.sql
COPY ./compare-flat.sh /tmp/compare-flat.sh
RUN chmod +x /tmp/compare-flat.sh \
    && if [ "$INCLUDE_DUCKDB" = "1" ]; then \
        apt-get update -y \
        && apt-get install -y --no-install-recommends wget unzip time ca-certificates \
        && wget -q https://github.com/duckdb/duckdb/releases/download/v$DUCKDB_VERSION/duckdb_cli-linux-amd64.zip -O /tmp/duckdb.zip \
        && echo "$DUCKDB_SHA256  /tmp/duckdb.zip" | sha256sum -c - \
        && unzip -q /tmp/duckdb.zip -d /usr/local/bin \
        && rm /tmp/duckdb.zip \
        && rm -rf /var/lib/apt/lists/*; \
    fi

######################################################################################
# Environment variables — runtime configuration
######################################################################################
# Scaling and parallelism
ENV SF=1
ENV BEXHOMA_NUM_PODS=4
ENV BEXHOMA_CHILD=1

# Data storage
ENV STORE_RAW_DATA=0
ENV STORE_RAW_DATA_RECREATE=0

# Schema variant and flat generation
ENV SSB_SCHEMA_VARIANT=normal
ENV SSB_WORK_DIR=/work
ENV SSB_SORT_MEM=512M
ENV SSB_FLAT_RESTORE_ORDER=1

# Bexhoma experiment identity
ENV BEXHOMA_CONNECTION=postgresql
ENV BEXHOMA_EXPERIMENT=12345
ENV BEXHOMA_EXPERIMENT_RUN=1
ENV BEXHOMA_CONFIGURATION=""
ENV BEXHOMA_CLIENT=1

# Pod synchronisation
ENV BEXHOMA_SYNCH_GENERATE=0

######################################################################################
# Working directory and data folders
######################################################################################
WORKDIR /tmp
RUN mkdir -p /tmp/ssb /work

######################################################################################
# Entrypoint
######################################################################################
CMD ["/bin/bash", "-c", "/tmp/generator.sh"]
