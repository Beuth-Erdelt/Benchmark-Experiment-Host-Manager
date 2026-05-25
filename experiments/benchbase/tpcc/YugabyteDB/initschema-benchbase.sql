-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/YugabyteDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: YugabyteDB TPC-C schema for benchbase. Uses YugabyteDB HASH/ASC
--          primary key syntax for tablet distribution. FK constraints are
--          omitted (not enforced on distributed tables). Waits 300 s after
--          creation to allow tablet splitting to complete.

CREATE TABLE warehouse (
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

CREATE TABLE item (
    i_id     INTEGER        NOT NULL,
    i_name   VARCHAR(24)    NOT NULL,
    i_price  NUMERIC(5, 2)  NOT NULL,
    i_data   VARCHAR(50)    NOT NULL,
    i_im_id  INTEGER        NOT NULL,
    CONSTRAINT item_pkey PRIMARY KEY (i_id)
);

CREATE TABLE stock (
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
    CONSTRAINT stock_pkey PRIMARY KEY (s_w_id HASH, s_i_id ASC)
    -- stock→item FK not applied: not supported on YugabyteDB distributed tables
    -- stock→warehouse FK not applied: not supported on YugabyteDB distributed tables
);

CREATE TABLE district (
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
    CONSTRAINT district_pkey PRIMARY KEY ((d_w_id,d_id) HASH)
    -- district→warehouse FK not applied: not supported on YugabyteDB distributed tables
);

CREATE TABLE customer (
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
    CONSTRAINT customer_pkey PRIMARY KEY ((c_w_id,c_d_id) HASH,c_id)
    -- customer→district FK not applied: not supported on YugabyteDB distributed tables
);

CREATE TABLE history (
    h_c_id    INTEGER        NOT NULL,
    h_c_d_id  INTEGER        NOT NULL,
    h_c_w_id  INTEGER        NOT NULL,
    h_d_id    INTEGER        NOT NULL,
    h_w_id    INTEGER        NOT NULL,
    h_date    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP NOT NULL,
    h_amount  NUMERIC(6, 2)  NOT NULL,
    h_data    VARCHAR(24)    NOT NULL
    -- history→customer FK not applied: not supported on YugabyteDB distributed tables
    -- history→district FK not applied: not supported on YugabyteDB distributed tables
);

CREATE TABLE oorder (
    o_w_id        INTEGER    NOT NULL,
    o_d_id        INTEGER    NOT NULL,
    o_id          INTEGER    NOT NULL,
    o_c_id        INTEGER    NOT NULL,
    o_carrier_id  INTEGER NULL,
    o_ol_cnt      INTEGER    NOT NULL,
    o_all_local   INTEGER    NOT NULL,
    o_entry_d     TIMESTAMP  DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT oorder_o_w_id_o_d_id_o_c_id_o_id_key UNIQUE (o_w_id, o_d_id, o_c_id, o_id),
    CONSTRAINT oorder_pkey PRIMARY KEY ((o_w_id,o_d_id) HASH,o_id)
    -- oorder→customer FK not applied: not supported on YugabyteDB distributed tables
);

CREATE TABLE new_order (
    no_w_id  INTEGER  NOT NULL,
    no_d_id  INTEGER  NOT NULL,
    no_o_id  INTEGER  NOT NULL,
    CONSTRAINT new_order_pkey PRIMARY KEY ((no_w_id,no_d_id) HASH,no_o_id)
    -- new_order→oorder FK not applied: not supported on YugabyteDB distributed tables
);

CREATE TABLE order_line (
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
    CONSTRAINT order_line_pkey PRIMARY KEY ((ol_w_id,ol_d_id) HASH, ol_o_id,ol_number)
    -- order_line→stock FK not applied: not supported on YugabyteDB distributed tables
    -- order_line→oorder FK not applied: not supported on YugabyteDB distributed tables
);

SELECT current_timestamp AS "Time after creation";

SELECT pg_sleep(300);

SELECT current_timestamp AS "Time after waiting";
