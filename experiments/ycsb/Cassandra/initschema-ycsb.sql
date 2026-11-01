-- Benchmark-Experiment-Host-Manager | experiments/ycsb/Cassandra
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Creates the keyspace ycsb and the table usertable as expected by the
--          cassandra-cql binding of YCSB. CQL, run by cqlsh; the suffix .sql
--          makes bexhoma run it through loadData.

-- Replication factor is a DDL parameter (ddl-parameters.config)
CREATE KEYSPACE ycsb
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': {num_worker_replicas}};

CREATE TABLE ycsb.usertable (
    y_id    varchar PRIMARY KEY,
    field0  varchar,
    field1  varchar,
    field2  varchar,
    field3  varchar,
    field4  varchar,
    field5  varchar,
    field6  varchar,
    field7  varchar,
    field8  varchar,
    field9  varchar
);
