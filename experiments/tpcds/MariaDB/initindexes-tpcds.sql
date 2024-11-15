
-- Store Sales Fact Table
CREATE INDEX idx_store_sales_customer_id ON tpcds.store_sales (ss_customer_sk);
CREATE INDEX idx_store_sales_item_id ON tpcds.store_sales (ss_item_sk);
CREATE INDEX idx_store_sales_promo_id ON tpcds.store_sales (ss_promo_sk);
CREATE INDEX idx_store_sales_store_id ON tpcds.store_sales (ss_store_sk);
CREATE INDEX idx_store_sales_date_id ON tpcds.store_sales (ss_sold_date_sk);

-- Catalog Sales Fact Table
CREATE INDEX idx_catalog_sales_customer_id ON tpcds.catalog_sales (cs_bill_customer_sk);
CREATE INDEX idx_catalog_sales_ship_customer_id ON tpcds.catalog_sales (cs_ship_customer_sk);
CREATE INDEX idx_catalog_sales_item_id ON tpcds.catalog_sales (cs_item_sk);
CREATE INDEX idx_catalog_sales_promo_id ON tpcds.catalog_sales (cs_promo_sk);
CREATE INDEX idx_catalog_sales_warehouse_id ON tpcds.catalog_sales (cs_warehouse_sk);
CREATE INDEX idx_catalog_sales_date_id ON tpcds.catalog_sales (cs_sold_date_sk);

-- Web Sales Fact Table
CREATE INDEX idx_web_sales_customer_id ON tpcds.web_sales (ws_bill_customer_sk);
CREATE INDEX idx_web_sales_ship_customer_id ON tpcds.web_sales (ws_ship_customer_sk);
CREATE INDEX idx_web_sales_item_id ON tpcds.web_sales (ws_item_sk);
CREATE INDEX idx_web_sales_promo_id ON tpcds.web_sales (ws_promo_sk);
CREATE INDEX idx_web_sales_warehouse_id ON tpcds.web_sales (ws_warehouse_sk);
CREATE INDEX idx_web_sales_date_id ON tpcds.web_sales (ws_sold_date_sk);

-- Inventory Fact Table
CREATE INDEX idx_inventory_item_id ON tpcds.inventory (inv_item_sk);
CREATE INDEX idx_inventory_warehouse_id ON tpcds.inventory (inv_warehouse_sk);
CREATE INDEX idx_inventory_date_id ON tpcds.inventory (inv_date_sk);

-- Customer Address Table (for customer relationships)
CREATE INDEX idx_customer_address_id ON tpcds.customer (c_current_addr_sk);
CREATE INDEX idx_customer_birth_country ON tpcds.customer (c_birth_country);

-- Store Returns Table
CREATE INDEX idx_store_returns_customer_id ON tpcds.store_returns (sr_customer_sk);
CREATE INDEX idx_store_returns_item_id ON tpcds.store_returns (sr_item_sk);
CREATE INDEX idx_store_returns_date_id ON tpcds.store_returns (sr_returned_date_sk);
CREATE INDEX idx_store_returns_ticket_id ON tpcds.store_returns (sr_ticket_number);
CREATE INDEX idx_store_returns_store_id ON tpcds.store_returns (sr_store_sk);

-- Catalog Returns Table
CREATE INDEX idx_catalog_returns_customer_id ON tpcds.catalog_returns (cr_returning_customer_sk);
CREATE INDEX idx_catalog_returns_item_id ON tpcds.catalog_returns (cr_item_sk);
CREATE INDEX idx_catalog_returns_date_id ON tpcds.catalog_returns (cr_returned_date_sk);
CREATE INDEX idx_catalog_returns_order_number ON tpcds.catalog_returns (cr_order_number);
CREATE INDEX idx_catalog_returns_warehouse_id ON tpcds.catalog_returns (cr_warehouse_sk);

-- Web Returns Table
CREATE INDEX idx_web_returns_customer_id ON tpcds.web_returns (wr_returning_customer_sk);
CREATE INDEX idx_web_returns_item_id ON tpcds.web_returns (wr_item_sk);
CREATE INDEX idx_web_returns_date_id ON tpcds.web_returns (wr_returned_date_sk);
CREATE INDEX idx_web_returns_order_number ON tpcds.web_returns (wr_order_number);







-- Indexes for the catalog_sales table
CREATE INDEX idx_catalog_sales_order_ship_date ON tpcds.catalog_sales (cs_order_number, cs_ship_date_sk);
CREATE INDEX idx_catalog_sales_ship_addr ON tpcds.catalog_sales (cs_ship_addr_sk);
CREATE INDEX idx_catalog_sales_warehouse ON tpcds.catalog_sales (cs_warehouse_sk);
CREATE INDEX idx_catalog_sales_call_center ON tpcds.catalog_sales (cs_call_center_sk);

-- Index for catalog_returns table to speed up the NOT EXISTS subquery
CREATE INDEX idx_catalog_returns_order ON tpcds.catalog_returns (cr_order_number);

-- Indexes for the date_dim table
CREATE INDEX idx_date_dim_date_sk_date ON tpcds.date_dim (d_date_sk, d_date);

-- Indexes for customer_address table to filter by ca_address_sk and ca_state
CREATE INDEX idx_customer_address_sk_state ON tpcds.customer_address (ca_address_sk, ca_state);

-- Indexes for call_center table to filter by call_center_sk and county
CREATE INDEX idx_call_center_county ON tpcds.call_center (cc_call_center_sk, cc_county);


CREATE INDEX idx_customer_current_cdemo_sk ON tpcds.customer (c_current_cdemo_sk);
CREATE INDEX idx_customer_address_county ON tpcds.customer_address (ca_county);
CREATE INDEX idx_date_dim_year_moy ON tpcds.date_dim (d_year, d_moy, d_date_sk);
CREATE INDEX idx_date_dim_d_year ON tpcds.date_dim (d_year);
