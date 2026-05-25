-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Full benchbase-generated PostgreSQL TPC-C DDL with complete FK
--          constraints and indexes. Serves as a reference schema; the Citus
--          variant (initschema-benchbase.sql) removes constraints not supported
--          by distributed tables.

CREATE TABLE public.item (
    i_id     INTEGER        NOT NULL,
    i_name   VARCHAR(24)    NOT NULL,
    i_price  NUMERIC(5, 2)  NOT NULL,
    i_data   VARCHAR(50)    NOT NULL,
    i_im_id  INTEGER        NOT NULL,
    CONSTRAINT item_pkey PRIMARY KEY (i_id)
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
    CONSTRAINT district_pkey PRIMARY KEY (d_w_id, d_id),
    CONSTRAINT district_d_w_id_fkey FOREIGN KEY (d_w_id) REFERENCES public.warehouse(w_id) ON DELETE CASCADE
);

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
    CONSTRAINT stock_pkey PRIMARY KEY (s_w_id, s_i_id),
    CONSTRAINT stock_s_i_id_fkey FOREIGN KEY (s_i_id) REFERENCES public.item(i_id) ON DELETE CASCADE,
    CONSTRAINT stock_s_w_id_fkey FOREIGN KEY (s_w_id) REFERENCES public.warehouse(w_id) ON DELETE CASCADE
);

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
    CONSTRAINT customer_pkey PRIMARY KEY (c_w_id, c_d_id, c_id),
    CONSTRAINT customer_c_w_id_c_d_id_fkey FOREIGN KEY (c_w_id,c_d_id) REFERENCES public.district(d_w_id,d_id) ON DELETE CASCADE
);
CREATE INDEX idx_customer_name ON public.customer USING BTREE (c_w_id, c_d_id, c_last, c_first);

CREATE TABLE public.history (
    h_c_id    INTEGER        NOT NULL,
    h_c_d_id  INTEGER        NOT NULL,
    h_c_w_id  INTEGER        NOT NULL,
    h_d_id    INTEGER        NOT NULL,
    h_w_id    INTEGER        NOT NULL,
    h_date    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP NOT NULL,
    h_amount  NUMERIC(6, 2)  NOT NULL,
    h_data    VARCHAR(24)    NOT NULL,
    CONSTRAINT history_h_c_w_id_h_c_d_id_h_c_id_fkey FOREIGN KEY (h_c_w_id,h_c_d_id,h_c_id) REFERENCES public.customer(c_w_id,c_d_id,c_id) ON DELETE CASCADE,
    CONSTRAINT history_h_w_id_h_d_id_fkey FOREIGN KEY (h_w_id,h_d_id) REFERENCES public.district(d_w_id,d_id) ON DELETE CASCADE
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
    CONSTRAINT oorder_o_w_id_o_d_id_o_c_id_o_id_key UNIQUE (o_w_id, o_d_id, o_c_id, o_id),
    CONSTRAINT oorder_pkey PRIMARY KEY (o_w_id, o_d_id, o_id),
    CONSTRAINT oorder_o_w_id_o_d_id_o_c_id_fkey FOREIGN KEY (o_w_id,o_d_id,o_c_id) REFERENCES public.customer(c_w_id,c_d_id,c_id) ON DELETE CASCADE
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
    CONSTRAINT order_line_pkey PRIMARY KEY (ol_w_id, ol_d_id, ol_o_id, ol_number),
    CONSTRAINT order_line_ol_supply_w_id_ol_i_id_fkey FOREIGN KEY (ol_supply_w_id,ol_i_id) REFERENCES public.stock(s_w_id,s_i_id) ON DELETE CASCADE,
    CONSTRAINT order_line_ol_w_id_ol_d_id_ol_o_id_fkey FOREIGN KEY (ol_w_id,ol_d_id,ol_o_id) REFERENCES public.oorder(o_w_id,o_d_id,o_id) ON DELETE CASCADE
);

CREATE TABLE public.new_order (
    no_w_id  INTEGER  NOT NULL,
    no_d_id  INTEGER  NOT NULL,
    no_o_id  INTEGER  NOT NULL,
    CONSTRAINT new_order_pkey PRIMARY KEY (no_w_id, no_d_id, no_o_id),
    CONSTRAINT new_order_no_w_id_no_d_id_no_o_id_fkey FOREIGN KEY (no_w_id,no_d_id,no_o_id) REFERENCES public.oorder(o_w_id,o_d_id,o_id) ON DELETE CASCADE
);
