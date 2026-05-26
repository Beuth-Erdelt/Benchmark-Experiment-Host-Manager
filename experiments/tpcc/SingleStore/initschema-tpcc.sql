-- Benchmark-Experiment-Host-Manager | experiments/tpcc/SingleStore
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: TPC-C schema for SingleStore using columnstore tables. All tables
--          use USING CLUSTERED COLUMNSTORE with USING HASH unique keys and
--          SHARD KEY distribution; item is a reference table replicated to
--          all nodes.

CREATE DATABASE tpcc;
USE tpcc;

CREATE TABLE warehouse (
    w_id        INT           NOT NULL,
    w_name      VARCHAR(10),
    w_street_1  VARCHAR(20),
    w_street_2  VARCHAR(20),
    w_city      VARCHAR(20),
    w_state     CHAR(2),
    w_zip       CHAR(9),
    w_tax       DECIMAL(4,2),
    w_ytd       DECIMAL(12,2),
    PRIMARY KEY (w_id),
    SHARD KEY (w_id)
);

CREATE TABLE district (
    d_id          TINYINT      NOT NULL,
    d_w_id        INT          NOT NULL,
    d_name        VARCHAR(10),
    d_street_1    VARCHAR(20),
    d_street_2    VARCHAR(20),
    d_city        VARCHAR(20),
    d_state       CHAR(2),
    d_zip         CHAR(9),
    d_tax         DECIMAL(4,2),
    d_ytd         DECIMAL(12,2),
    d_next_o_id   INT,
    PRIMARY KEY (d_w_id, d_id),
    SHARD KEY (d_w_id)
);

CREATE TABLE customer (
    c_id            INT          NOT NULL,
    c_d_id          TINYINT      NOT NULL,
    c_w_id          INT          NOT NULL,
    c_first         VARCHAR(16),
    c_middle        CHAR(2),
    c_last          VARCHAR(16),
    c_street_1      VARCHAR(20),
    c_street_2      VARCHAR(20),
    c_city          VARCHAR(20),
    c_state         CHAR(2),
    c_zip           CHAR(9),
    c_phone         CHAR(16),
    c_since         DATETIME,
    c_credit        CHAR(2),
    c_credit_lim    BIGINT,
    c_discount      DECIMAL(4,2),
    c_balance       DECIMAL(12,2),
    c_ytd_payment   DECIMAL(12,2),
    c_payment_cnt   SMALLINT,
    c_delivery_cnt  SMALLINT,
    c_data          TEXT,
    KEY (c_w_id, c_d_id, c_id) USING CLUSTERED COLUMNSTORE,
    UNIQUE KEY (c_w_id, c_d_id, c_id) USING HASH,
    KEY (c_last) USING HASH,
    SHARD KEY (c_w_id)
);

CREATE TABLE history (
    h_c_id    INT,
    h_c_d_id  TINYINT,
    h_c_w_id  INT,
    h_d_id    TINYINT,
    h_w_id    INT,
    h_date    DATETIME,
    h_amount  DECIMAL(6,2),
    h_data    VARCHAR(24),
    KEY () USING CLUSTERED COLUMNSTORE,
    SHARD KEY (h_c_w_id)
);

CREATE TABLE new_orders (
    no_o_id  INT      NOT NULL,
    no_d_id  TINYINT  NOT NULL,
    no_w_id  INT      NOT NULL,
    KEY (no_w_id, no_d_id, no_o_id) USING CLUSTERED COLUMNSTORE,
    UNIQUE KEY (no_w_id, no_d_id, no_o_id) USING HASH,
    SHARD KEY (no_w_id)
);

CREATE TABLE orders (
    o_id          INT      NOT NULL,
    o_d_id        TINYINT  NOT NULL,
    o_w_id        INT      NOT NULL,
    o_c_id        INT,
    o_entry_d     DATETIME,
    o_carrier_id  TINYINT,
    o_ol_cnt      TINYINT,
    o_all_local   TINYINT,
    KEY (o_w_id, o_d_id, o_id) USING CLUSTERED COLUMNSTORE,
    UNIQUE KEY (o_w_id, o_d_id, o_id) USING HASH,
    SHARD KEY (o_w_id)
);

CREATE TABLE order_line (
    ol_o_id          INT      NOT NULL,
    ol_d_id          TINYINT  NOT NULL,
    ol_w_id          INT      NOT NULL,
    ol_number        TINYINT  NOT NULL,
    ol_i_id          INT,
    ol_supply_w_id   INT,
    ol_delivery_d    DATETIME,
    ol_quantity      TINYINT,
    ol_amount        DECIMAL(6,2),
    ol_dist_info     CHAR(24),
    KEY (ol_w_id, ol_d_id, ol_o_id, ol_number) USING CLUSTERED COLUMNSTORE,
    UNIQUE KEY (ol_w_id, ol_d_id, ol_o_id, ol_number) USING HASH,
    SHARD KEY (ol_w_id)
);

CREATE REFERENCE TABLE item (
    i_id     INT  NOT NULL,
    i_im_id  INT,
    i_name   VARCHAR(24),
    i_price  DECIMAL(5,2),
    i_data   VARCHAR(50),
    KEY () USING CLUSTERED COLUMNSTORE,
    UNIQUE KEY (i_id) USING HASH
);

CREATE TABLE stock (
    s_i_id        INT   NOT NULL,
    s_w_id        INT   NOT NULL,
    s_quantity    SMALLINT,
    s_dist_01     CHAR(24),
    s_dist_02     CHAR(24),
    s_dist_03     CHAR(24),
    s_dist_04     CHAR(24),
    s_dist_05     CHAR(24),
    s_dist_06     CHAR(24),
    s_dist_07     CHAR(24),
    s_dist_08     CHAR(24),
    s_dist_09     CHAR(24),
    s_dist_10     CHAR(24),
    s_ytd         DECIMAL(8,0),
    s_order_cnt   SMALLINT,
    s_remote_cnt  SMALLINT,
    s_data        VARCHAR(50),
    KEY (s_w_id, s_i_id) USING CLUSTERED COLUMNSTORE,
    UNIQUE KEY (s_w_id, s_i_id) USING HASH,
    SHARD KEY (s_w_id)
);
