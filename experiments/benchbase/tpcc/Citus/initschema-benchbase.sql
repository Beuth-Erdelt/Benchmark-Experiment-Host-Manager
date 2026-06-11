-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Citus TPC-C schema for benchbase, derived from the benchbase
--          PostgreSQL DDL. FK constraints are omitted (not supported on Citus
--          distributed tables). Includes Citus shard distribution commands.

CREATE TABLE public.customer (
    c_w_id          INTEGER         NOT NULL,
    c_d_id          INTEGER         NOT NULL,
    c_id            INTEGER         NOT NULL,
    c_discount      NUMERIC(4, 4)   NOT NULL,
    c_credit        CHAR(2)         NOT NULL,
    c_last          VARCHAR(16)     NOT NULL,
    c_first         VARCHAR(16)     NOT NULL,
    c_credit_lim    NUMERIC(12, 2)  NOT NULL,
    c_balance       NUMERIC(12, 2)  NOT NULL,
    c_ytd_payment   FLOAT8          NOT NULL,
    c_payment_cnt   INTEGER         NOT NULL,
    c_delivery_cnt  INTEGER         NOT NULL,
    c_street_1      VARCHAR(20)     NOT NULL,
    c_street_2      VARCHAR(20)     NOT NULL,
    c_city          VARCHAR(20)     NOT NULL,
    c_state         CHAR(2)         NOT NULL,
    c_zip           CHAR(9)         NOT NULL,
    c_phone         CHAR(16)        NOT NULL,
    c_since         TIMESTAMP       DEFAULT CURRENT_TIMESTAMP NOT NULL,
    c_middle        CHAR(2)         NOT NULL,
    c_data          VARCHAR(500)    NOT NULL,
    CONSTRAINT customer_pkey PRIMARY KEY (c_w_id, c_d_id, c_id)
    -- customer->district FK not applied: not supported on Citus distributed tables
);

CREATE TABLE public.district (
    d_w_id       INTEGER         NOT NULL,
    d_id         INTEGER         NOT NULL,
    d_ytd        NUMERIC(12, 2)  NOT NULL,
    d_tax        NUMERIC(4, 4)   NOT NULL,
    d_next_o_id  INTEGER         NOT NULL,
    d_name       VARCHAR(10)     NOT NULL,
    d_street_1   VARCHAR(20)     NOT NULL,
    d_street_2   VARCHAR(20)     NOT NULL,
    d_city       VARCHAR(20)     NOT NULL,
    d_state      CHAR(2)         NOT NULL,
    d_zip        CHAR(9)         NOT NULL,
    CONSTRAINT district_pkey PRIMARY KEY (d_w_id, d_id)
    -- district->warehouse FK not applied: not supported on Citus distributed tables
);

CREATE TABLE public.history (
    h_c_id    INTEGER        NOT NULL,
    h_c_d_id  INTEGER        NOT NULL,
    h_c_w_id  INTEGER        NOT NULL,
    h_d_id    INTEGER        NOT NULL,
    h_w_id    INTEGER        NOT NULL,
    h_date    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP NOT NULL,
    h_amount  NUMERIC(6, 2)  NOT NULL,
    h_data    VARCHAR(24)    NOT NULL
    -- history->customer FK not applied: not supported on Citus distributed tables
    -- history->district FK not applied: not supported on Citus distributed tables
);

CREATE TABLE public.item (
    i_id     INTEGER        NOT NULL,
    i_name   VARCHAR(24)    NOT NULL,
    i_price  NUMERIC(5, 2)  NOT NULL,
    i_data   VARCHAR(50)    NOT NULL,
    i_im_id  INTEGER        NOT NULL,
    CONSTRAINT item_pkey PRIMARY KEY (i_id)
);

CREATE TABLE public.new_order (
    no_w_id  INTEGER  NOT NULL,
    no_d_id  INTEGER  NOT NULL,
    no_o_id  INTEGER  NOT NULL,
    CONSTRAINT new_order_pkey PRIMARY KEY (no_w_id, no_d_id, no_o_id)
    -- new_order->oorder FK not applied: not supported on Citus distributed tables
);

CREATE TABLE public.order_line (
    ol_w_id         INTEGER        NOT NULL,
    ol_d_id         INTEGER        NOT NULL,
    ol_o_id         INTEGER        NOT NULL,
    ol_number       INTEGER        NOT NULL,
    ol_i_id         INTEGER        NOT NULL,
    ol_delivery_d   TIMESTAMP NULL,
    ol_amount       NUMERIC(6, 2)  NOT NULL,
    ol_supply_w_id  INTEGER        NOT NULL,
    ol_quantity     NUMERIC(6, 2)  NOT NULL,
    ol_dist_info    CHAR(24)       NOT NULL,
    CONSTRAINT order_line_pkey PRIMARY KEY (ol_w_id, ol_d_id, ol_o_id, ol_number)
    -- order_line->stock FK not applied: not supported on Citus distributed tables
    -- order_line->oorder FK not applied: not supported on Citus distributed tables
);

CREATE TABLE public.oorder (
    o_w_id        INTEGER    NOT NULL,
    o_d_id        INTEGER    NOT NULL,
    o_id          INTEGER    NOT NULL,
    o_c_id        INTEGER    NOT NULL,
    o_carrier_id  INTEGER NULL,
    o_ol_cnt      INTEGER    NOT NULL,
    o_all_local   INTEGER    NOT NULL,
    o_entry_d     TIMESTAMP  DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT oorder_pkey PRIMARY KEY (o_w_id, o_d_id, o_id)
    -- oorder->customer FK not applied: not supported on Citus distributed tables
);
CREATE UNIQUE INDEX oorder_i2 ON public.oorder USING BTREE (o_w_id, o_d_id, o_c_id, o_id);

CREATE TABLE public.stock (
    s_w_id        INTEGER        NOT NULL,
    s_i_id        INTEGER        NOT NULL,
    s_quantity    INTEGER        NOT NULL,
    s_ytd         NUMERIC(8, 2)  NOT NULL,
    s_order_cnt   INTEGER        NOT NULL,
    s_remote_cnt  INTEGER        NOT NULL,
    s_data        VARCHAR(50)    NOT NULL,
    s_dist_01     CHAR(24)       NOT NULL,
    s_dist_02     CHAR(24)       NOT NULL,
    s_dist_03     CHAR(24)       NOT NULL,
    s_dist_04     CHAR(24)       NOT NULL,
    s_dist_05     CHAR(24)       NOT NULL,
    s_dist_06     CHAR(24)       NOT NULL,
    s_dist_07     CHAR(24)       NOT NULL,
    s_dist_08     CHAR(24)       NOT NULL,
    s_dist_09     CHAR(24)       NOT NULL,
    s_dist_10     CHAR(24)       NOT NULL,
    CONSTRAINT stock_pkey PRIMARY KEY (s_w_id, s_i_id)
    -- stock->item FK not applied: not supported on Citus distributed tables
    -- stock->warehouse FK not applied: not supported on Citus distributed tables
);

CREATE TABLE public.warehouse (
    w_id        INTEGER         NOT NULL,
    w_ytd       NUMERIC(12, 2)  NOT NULL,
    w_tax       NUMERIC(4, 4)   NOT NULL,
    w_name      VARCHAR(10)     NOT NULL,
    w_street_1  VARCHAR(20)     NOT NULL,
    w_street_2  VARCHAR(20)     NOT NULL,
    w_city      VARCHAR(20)     NOT NULL,
    w_state     CHAR(2)         NOT NULL,
    w_zip       CHAR(9)         NOT NULL,
    CONSTRAINT warehouse_pkey PRIMARY KEY (w_id)
);

SELECT create_distributed_table('customer', 'c_w_id');
SELECT create_distributed_table('district', 'd_w_id');
SELECT create_distributed_table('history', 'h_w_id');
SELECT create_distributed_table('warehouse', 'w_id');
SELECT create_distributed_table('stock', 's_w_id');
SELECT create_distributed_table('new_order', 'no_w_id');
SELECT create_distributed_table('oorder', 'o_w_id');
SELECT create_distributed_table('order_line', 'ol_w_id');
SELECT create_reference_table('item');

-- Verify Distribution
SELECT * FROM citus_shards;

SELECT 'pg_stat_replication' AS message;
SELECT * FROM pg_stat_replication;

SELECT 'pg_dist_partition' AS message;
SELECT * FROM pg_dist_partition;

SELECT 'pg_dist_shard' AS message;
SELECT * FROM pg_dist_shard;

SELECT 'citus_shards' AS message;
SELECT * FROM citus_shards;

SELECT 'pg_dist_placement' AS message;
SELECT * FROM pg_dist_placement;

SELECT 'pg_dist_node' AS message;
SELECT * FROM pg_dist_node;

SELECT 'citus_tables' AS message;
SELECT * FROM citus_tables;

SELECT 'citus_get_active_worker_nodes' AS message;
SELECT * FROM citus_get_active_worker_nodes();
