-- Benchmark-Experiment-Host-Manager | experiments/tpcds/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create secondary indexes on the TPC-DS tables for PostgreSQL.
--          Run after initconstraints-tpcds.sql.

-- Store sales fact table
CREATE INDEX idx_store_sales_date_id     ON public.store_sales (ss_sold_date_sk);
CREATE INDEX idx_store_sales_customer_id ON public.store_sales (ss_customer_sk);
CREATE INDEX idx_store_sales_item_id     ON public.store_sales (ss_item_sk);
CREATE INDEX idx_store_sales_store_id    ON public.store_sales (ss_store_sk);
CREATE INDEX idx_store_sales_promo_id    ON public.store_sales (ss_promo_sk);

-- Catalog sales fact table
CREATE INDEX idx_catalog_sales_date_id         ON public.catalog_sales (cs_sold_date_sk);
CREATE INDEX idx_catalog_sales_customer_id     ON public.catalog_sales (cs_bill_customer_sk);
CREATE INDEX idx_catalog_sales_ship_customer_id ON public.catalog_sales (cs_ship_customer_sk);
CREATE INDEX idx_catalog_sales_item_id         ON public.catalog_sales (cs_item_sk);
CREATE INDEX idx_catalog_sales_promo_id        ON public.catalog_sales (cs_promo_sk);
CREATE INDEX idx_catalog_sales_warehouse_id    ON public.catalog_sales (cs_warehouse_sk);
CREATE INDEX idx_catalog_sales_order_ship_date ON public.catalog_sales (cs_order_number, cs_ship_date_sk);
CREATE INDEX idx_catalog_sales_ship_addr       ON public.catalog_sales (cs_ship_addr_sk);
CREATE INDEX idx_catalog_sales_call_center     ON public.catalog_sales (cs_call_center_sk);

-- Web sales fact table
CREATE INDEX idx_web_sales_date_id          ON public.web_sales (ws_sold_date_sk);
CREATE INDEX idx_web_sales_customer_id      ON public.web_sales (ws_bill_customer_sk);
CREATE INDEX idx_web_sales_ship_customer_id ON public.web_sales (ws_ship_customer_sk);
CREATE INDEX idx_web_sales_item_id          ON public.web_sales (ws_item_sk);
CREATE INDEX idx_web_sales_promo_id         ON public.web_sales (ws_promo_sk);
CREATE INDEX idx_web_sales_warehouse_id     ON public.web_sales (ws_warehouse_sk);
CREATE INDEX idx_web_sales_order_number     ON public.web_sales (ws_order_number);
CREATE INDEX idx_web_sales_ship_date        ON public.web_sales (ws_ship_date_sk);
CREATE INDEX idx_web_sales_addr             ON public.web_sales (ws_ship_addr_sk);
CREATE INDEX idx_web_sales_web_site         ON public.web_sales (ws_web_site_sk);

-- Inventory fact table
CREATE INDEX idx_inventory_date_id      ON public.inventory (inv_date_sk);
CREATE INDEX idx_inventory_item_id      ON public.inventory (inv_item_sk);
CREATE INDEX idx_inventory_warehouse_id ON public.inventory (inv_warehouse_sk);

-- Store returns table
CREATE INDEX idx_store_returns_date_id      ON public.store_returns (sr_returned_date_sk);
CREATE INDEX idx_store_returns_customer_id  ON public.store_returns (sr_customer_sk);
CREATE INDEX idx_store_returns_item_id      ON public.store_returns (sr_item_sk);
CREATE INDEX idx_store_returns_store_id     ON public.store_returns (sr_store_sk);
CREATE INDEX idx_store_returns_ticket_id    ON public.store_returns (sr_ticket_number);

-- Catalog returns table
CREATE INDEX idx_catalog_returns_date_id      ON public.catalog_returns (cr_returned_date_sk);
CREATE INDEX idx_catalog_returns_customer_id  ON public.catalog_returns (cr_returning_customer_sk);
CREATE INDEX idx_catalog_returns_item_id      ON public.catalog_returns (cr_item_sk);
CREATE INDEX idx_catalog_returns_order_number ON public.catalog_returns (cr_order_number);
CREATE INDEX idx_catalog_returns_order        ON public.catalog_returns (cr_order_number);
CREATE INDEX idx_catalog_returns_warehouse_id ON public.catalog_returns (cr_warehouse_sk);

-- Web returns table
CREATE INDEX idx_web_returns_date_id      ON public.web_returns (wr_returned_date_sk);
CREATE INDEX idx_web_returns_customer_id  ON public.web_returns (wr_returning_customer_sk);
CREATE INDEX idx_web_returns_item_id      ON public.web_returns (wr_item_sk);
CREATE INDEX idx_web_returns_order_number ON public.web_returns (wr_order_number);

-- Customer table
CREATE INDEX idx_customer_address_id       ON public.customer (c_current_addr_sk);
CREATE INDEX idx_customer_current_cdemo_sk ON public.customer (c_current_cdemo_sk);
CREATE INDEX idx_customer_birth_country    ON public.customer (c_birth_country);

-- Customer address table
CREATE INDEX idx_customer_address_sk_state ON public.customer_address (ca_address_sk, ca_state);
CREATE INDEX idx_customer_address_county   ON public.customer_address (ca_county);

-- Date dimension table
CREATE INDEX idx_date_dim_date_sk_date ON public.date_dim (d_date_sk, d_date);
CREATE INDEX idx_date_dim_year_moy     ON public.date_dim (d_year, d_moy, d_date_sk);
CREATE INDEX idx_date_dim_d_year       ON public.date_dim (d_year);

-- Call center table
CREATE INDEX idx_call_center_county ON public.call_center (cc_call_center_sk, cc_county);

-- Web site table
CREATE INDEX idx_web_site_company ON public.web_site (web_site_sk, web_company_name);
