-- Benchmark-Experiment-Host-Manager | experiments/tpcds/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-DS data at scale factor 100 (SF100 ~ 100 GB) into PostgreSQL.
--          See initdata-tpcds-SF1.sql for format details.

COPY public.call_center             FROM '/data/tpcds/SF100/call_center.dat'             DELIMITER '|' NULL '';
COPY public.catalog_page            FROM '/data/tpcds/SF100/catalog_page.dat'            DELIMITER '|' NULL '';
COPY public.catalog_returns         FROM '/data/tpcds/SF100/catalog_returns.dat'         DELIMITER '|' NULL '';
COPY public.catalog_sales           FROM '/data/tpcds/SF100/catalog_sales.dat'           DELIMITER '|' NULL '';
COPY public.customer                FROM '/data/tpcds/SF100/customer.dat'                DELIMITER '|' NULL '';
COPY public.customer_address        FROM '/data/tpcds/SF100/customer_address.dat'        DELIMITER '|' NULL '';
COPY public.customer_demographics   FROM '/data/tpcds/SF100/customer_demographics.dat'   DELIMITER '|' NULL '';
COPY public.date_dim                FROM '/data/tpcds/SF100/date_dim.dat'                DELIMITER '|' NULL '';
COPY public.dbgen_version           FROM '/data/tpcds/SF100/dbgen_version.dat'           DELIMITER '|' NULL '';
COPY public.household_demographics  FROM '/data/tpcds/SF100/household_demographics.dat'  DELIMITER '|' NULL '';
COPY public.income_band             FROM '/data/tpcds/SF100/income_band.dat'             DELIMITER '|' NULL '';
COPY public.inventory               FROM '/data/tpcds/SF100/inventory.dat'               DELIMITER '|' NULL '';
COPY public.item                    FROM '/data/tpcds/SF100/item.dat'                    DELIMITER '|' NULL '';
COPY public.promotion               FROM '/data/tpcds/SF100/promotion.dat'               DELIMITER '|' NULL '';
COPY public.reason                  FROM '/data/tpcds/SF100/reason.dat'                  DELIMITER '|' NULL '';
COPY public.ship_mode               FROM '/data/tpcds/SF100/ship_mode.dat'               DELIMITER '|' NULL '';
COPY public.store                   FROM '/data/tpcds/SF100/store.dat'                   DELIMITER '|' NULL '';
COPY public.store_returns           FROM '/data/tpcds/SF100/store_returns.dat'           DELIMITER '|' NULL '';
COPY public.store_sales             FROM '/data/tpcds/SF100/store_sales.dat'             DELIMITER '|' NULL '';
COPY public.time_dim                FROM '/data/tpcds/SF100/time_dim.dat'                DELIMITER '|' NULL '';
COPY public.warehouse               FROM '/data/tpcds/SF100/warehouse.dat'               DELIMITER '|' NULL '';
COPY public.web_page                FROM '/data/tpcds/SF100/web_page.dat'                DELIMITER '|' NULL '';
COPY public.web_returns             FROM '/data/tpcds/SF100/web_returns.dat'             DELIMITER '|' NULL '';
COPY public.web_sales               FROM '/data/tpcds/SF100/web_sales.dat'               DELIMITER '|' NULL '';
COPY public.web_site                FROM '/data/tpcds/SF100/web_site.dat'                DELIMITER '|' NULL '';
