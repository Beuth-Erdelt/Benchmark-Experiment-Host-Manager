-- Benchmark-Experiment-Host-Manager | experiments/tpcds/DB2
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Secondary indexes on the foreign key columns of the TPC-DS fact
--          tables (the same as for PostgreSQL). The primary keys are declared in
--          initschema-tpcds.sql. Runs in the schema DB2INST1 (default schema of
--          the CLP session of /tmp/bexhoma-run.sh).
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX idx_store_sales_date_id     ON store_sales (ss_sold_date_sk);
CREATE INDEX idx_store_sales_customer_id ON store_sales (ss_customer_sk);
CREATE INDEX idx_store_sales_item_id     ON store_sales (ss_item_sk);
CREATE INDEX idx_store_sales_store_id    ON store_sales (ss_store_sk);
CREATE INDEX idx_store_sales_promo_id    ON store_sales (ss_promo_sk);

-- Catalog sales fact table
CREATE INDEX idx_catalog_sales_date_id         ON catalog_sales (cs_sold_date_sk);
CREATE INDEX idx_catalog_sales_customer_id     ON catalog_sales (cs_bill_customer_sk);
CREATE INDEX idx_catalog_sales_ship_customer_id ON catalog_sales (cs_ship_customer_sk);
CREATE INDEX idx_catalog_sales_item_id         ON catalog_sales (cs_item_sk);
CREATE INDEX idx_catalog_sales_promo_id        ON catalog_sales (cs_promo_sk);
CREATE INDEX idx_catalog_sales_warehouse_id    ON catalog_sales (cs_warehouse_sk);
CREATE INDEX idx_catalog_sales_order_ship_date ON catalog_sales (cs_order_number, cs_ship_date_sk);
CREATE INDEX idx_catalog_sales_ship_addr       ON catalog_sales (cs_ship_addr_sk);
CREATE INDEX idx_catalog_sales_call_center     ON catalog_sales (cs_call_center_sk);

-- Web sales fact table
CREATE INDEX idx_web_sales_date_id          ON web_sales (ws_sold_date_sk);
CREATE INDEX idx_web_sales_customer_id      ON web_sales (ws_bill_customer_sk);
CREATE INDEX idx_web_sales_ship_customer_id ON web_sales (ws_ship_customer_sk);
CREATE INDEX idx_web_sales_item_id          ON web_sales (ws_item_sk);
CREATE INDEX idx_web_sales_promo_id         ON web_sales (ws_promo_sk);
CREATE INDEX idx_web_sales_warehouse_id     ON web_sales (ws_warehouse_sk);
CREATE INDEX idx_web_sales_order_number     ON web_sales (ws_order_number);
CREATE INDEX idx_web_sales_ship_date        ON web_sales (ws_ship_date_sk);
CREATE INDEX idx_web_sales_addr             ON web_sales (ws_ship_addr_sk);
CREATE INDEX idx_web_sales_web_site         ON web_sales (ws_web_site_sk);

-- Inventory fact table
CREATE INDEX idx_inventory_date_id      ON inventory (inv_date_sk);
CREATE INDEX idx_inventory_item_id      ON inventory (inv_item_sk);
CREATE INDEX idx_inventory_warehouse_id ON inventory (inv_warehouse_sk);

-- Store returns table
CREATE INDEX idx_store_returns_date_id      ON store_returns (sr_returned_date_sk);
CREATE INDEX idx_store_returns_customer_id  ON store_returns (sr_customer_sk);
CREATE INDEX idx_store_returns_item_id      ON store_returns (sr_item_sk);
CREATE INDEX idx_store_returns_store_id     ON store_returns (sr_store_sk);
CREATE INDEX idx_store_returns_ticket_id    ON store_returns (sr_ticket_number);

-- Catalog returns table
CREATE INDEX idx_catalog_returns_date_id      ON catalog_returns (cr_returned_date_sk);
CREATE INDEX idx_catalog_returns_customer_id  ON catalog_returns (cr_returning_customer_sk);
CREATE INDEX idx_catalog_returns_item_id      ON catalog_returns (cr_item_sk);
CREATE INDEX idx_catalog_returns_order_number ON catalog_returns (cr_order_number);
CREATE INDEX idx_catalog_returns_order        ON catalog_returns (cr_order_number);
CREATE INDEX idx_catalog_returns_warehouse_id ON catalog_returns (cr_warehouse_sk);

-- Web returns table
CREATE INDEX idx_web_returns_date_id      ON web_returns (wr_returned_date_sk);
CREATE INDEX idx_web_returns_customer_id  ON web_returns (wr_returning_customer_sk);
CREATE INDEX idx_web_returns_item_id      ON web_returns (wr_item_sk);
CREATE INDEX idx_web_returns_order_number ON web_returns (wr_order_number);

-- Customer table
CREATE INDEX idx_customer_address_id       ON customer (c_current_addr_sk);
CREATE INDEX idx_customer_current_cdemo_sk ON customer (c_current_cdemo_sk);
CREATE INDEX idx_customer_birth_country    ON customer (c_birth_country);

-- Customer address table
CREATE INDEX idx_customer_address_sk_state ON customer_address (ca_address_sk, ca_state);
CREATE INDEX idx_customer_address_county   ON customer_address (ca_county);

-- Date dimension table
CREATE INDEX idx_date_dim_date_sk_date ON date_dim (d_date_sk, d_date);
CREATE INDEX idx_date_dim_year_moy     ON date_dim (d_year, d_moy, d_date_sk);
CREATE INDEX idx_date_dim_d_year       ON date_dim (d_year);

-- Call center table
CREATE INDEX idx_call_center_county ON call_center (cc_call_center_sk, cc_county);

-- Web site table
CREATE INDEX idx_web_site_company ON web_site (web_site_sk, web_company_name);
