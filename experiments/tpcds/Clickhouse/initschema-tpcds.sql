-- Benchmark-Experiment-Host-Manager | experiments/tpcds/Clickhouse
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create the 25 TPC-DS tables in the tpcds database for ClickHouse.
--          Uses MergeTree engine with explicit ORDER BY keys.
--          data_type_default_nullable=1 allows DEFAULT NULL on typed columns.

CREATE DATABASE tpcds;

SET data_type_default_nullable=1;
SET cast_keep_nullable = 1;

SELECT * FROM system.settings WHERE name LIKE '%null%';

CREATE TABLE tpcds.dbgen_version
(
    dv_version      String DEFAULT NULL,
    dv_create_date  Date   DEFAULT NULL,
    dv_create_time  String DEFAULT NULL,
    dv_cmdline_args String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY tuple()
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.customer_address
(
    ca_address_sk    Int32  NOT NULL,
    ca_address_id    String NOT NULL,
    ca_street_number String DEFAULT NULL,
    ca_street_name   String DEFAULT NULL,
    ca_street_type   String DEFAULT NULL,
    ca_suite_number  String DEFAULT NULL,
    ca_city          String DEFAULT NULL,
    ca_county        String DEFAULT NULL,
    ca_state         String DEFAULT NULL,
    ca_zip           String DEFAULT NULL,
    ca_country       String DEFAULT NULL,
    ca_gmt_offset    Float  DEFAULT NULL,
    ca_location_type String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY ca_address_sk
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.customer_demographics
(
    cd_demo_sk            Int32  NOT NULL,
    cd_gender             String DEFAULT NULL,
    cd_marital_status     String DEFAULT NULL,
    cd_education_status   String DEFAULT NULL,
    cd_purchase_estimate  Int32  DEFAULT NULL,
    cd_credit_rating      String DEFAULT NULL,
    cd_dep_count          Int32  DEFAULT NULL,
    cd_dep_employed_count Int32  DEFAULT NULL,
    cd_dep_college_count  Int32  DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY cd_demo_sk
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.date_dim
(
    d_date_sk           Int32  NOT NULL,
    d_date_id           String NOT NULL,
    d_date              Date   NOT NULL,
    d_month_seq         Int32  DEFAULT NULL,
    d_week_seq          Int32  DEFAULT NULL,
    d_quarter_seq       Int32  DEFAULT NULL,
    d_year              Int32  DEFAULT NULL,
    d_dow               Int32  DEFAULT NULL,
    d_moy               Int32  DEFAULT NULL,
    d_dom               Int32  DEFAULT NULL,
    d_qoy               Int32  DEFAULT NULL,
    d_fy_year           Int32  DEFAULT NULL,
    d_fy_quarter_seq    Int32  DEFAULT NULL,
    d_fy_week_seq       Int32  DEFAULT NULL,
    d_day_name          String DEFAULT NULL,
    d_quarter_name      String DEFAULT NULL,
    d_holiday           String DEFAULT NULL,
    d_weekend           String DEFAULT NULL,
    d_following_holiday String DEFAULT NULL,
    d_first_dom         Int32  DEFAULT NULL,
    d_last_dom          Int32  DEFAULT NULL,
    d_same_day_ly       Int32  DEFAULT NULL,
    d_same_day_lq       Int32  DEFAULT NULL,
    d_current_day       String DEFAULT NULL,
    d_current_week      String DEFAULT NULL,
    d_current_month     String DEFAULT NULL,
    d_current_quarter   String DEFAULT NULL,
    d_current_year      String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY d_date_sk;

CREATE TABLE tpcds.warehouse
(
    w_warehouse_sk    Int32  NOT NULL,
    w_warehouse_id    String NOT NULL,
    w_warehouse_name  String DEFAULT NULL,
    w_warehouse_sq_ft Int32  DEFAULT NULL,
    w_street_number   String DEFAULT NULL,
    w_street_name     String DEFAULT NULL,
    w_street_type     String DEFAULT NULL,
    w_suite_number    String DEFAULT NULL,
    w_city            String DEFAULT NULL,
    w_county          String DEFAULT NULL,
    w_state           String DEFAULT NULL,
    w_zip             String DEFAULT NULL,
    w_country         String DEFAULT NULL,
    w_gmt_offset      Float  DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY w_warehouse_sk;

CREATE TABLE tpcds.ship_mode
(
    sm_ship_mode_sk Int32  NOT NULL,
    sm_ship_mode_id String NOT NULL,
    sm_type         String DEFAULT NULL,
    sm_code         String DEFAULT NULL,
    sm_carrier      String DEFAULT NULL,
    sm_contract     String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY sm_ship_mode_sk
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.time_dim
(
    t_time_sk   Int32  NOT NULL,
    t_time_id   String NOT NULL,
    t_time      Int32  NOT NULL,
    t_hour      Int32  DEFAULT NULL,
    t_minute    Int32  DEFAULT NULL,
    t_second    Int32  DEFAULT NULL,
    t_am_pm     String DEFAULT NULL,
    t_shift     String DEFAULT NULL,
    t_sub_shift String DEFAULT NULL,
    t_meal_time String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY t_time_sk;

CREATE TABLE tpcds.reason
(
    r_reason_sk   Int32  NOT NULL,
    r_reason_id   String NOT NULL,
    r_reason_desc String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY r_reason_sk
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.income_band
(
    ib_income_band_sk Int32 NOT NULL,
    ib_lower_bound    Int32 DEFAULT NULL,
    ib_upper_bound    Int32 DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY ib_income_band_sk
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.item
(
    i_item_sk        Int32  NOT NULL,
    i_item_id        String NOT NULL,
    i_rec_start_date Date   DEFAULT NULL,
    i_rec_end_date   Date   DEFAULT NULL,
    i_item_desc      String DEFAULT NULL,
    i_current_price  Float  DEFAULT NULL,
    i_wholesale_cost Float  DEFAULT NULL,
    i_brand_id       Int32  DEFAULT NULL,
    i_brand          String DEFAULT NULL,
    i_class_id       Int32  DEFAULT NULL,
    i_class          String DEFAULT NULL,
    i_category_id    Int32  DEFAULT NULL,
    i_category       String DEFAULT NULL,
    i_manufact_id    Int32  DEFAULT NULL,
    i_manufact       String DEFAULT NULL,
    i_size           String DEFAULT NULL,
    i_formulation    String DEFAULT NULL,
    i_color          String DEFAULT NULL,
    i_units          String DEFAULT NULL,
    i_container      String DEFAULT NULL,
    i_manager_id     Int32  DEFAULT NULL,
    i_product_name   String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY i_item_sk;

CREATE TABLE tpcds.store
(
    s_store_sk         Int32  NOT NULL,
    s_store_id         String NOT NULL,
    s_rec_start_date   Date   DEFAULT NULL,
    s_rec_end_date     Date   DEFAULT NULL,
    s_closed_date_sk   Int32  DEFAULT NULL,
    s_store_name       String DEFAULT NULL,
    s_number_employees Int32  DEFAULT NULL,
    s_floor_space      Int32  DEFAULT NULL,
    s_hours            String DEFAULT NULL,
    s_manager          String DEFAULT NULL,
    s_market_id        Int32  DEFAULT NULL,
    s_geography_class  String DEFAULT NULL,
    s_market_desc      String DEFAULT NULL,
    s_market_manager   String DEFAULT NULL,
    s_division_id      Int32  DEFAULT NULL,
    s_division_name    String DEFAULT NULL,
    s_company_id       Int32  DEFAULT NULL,
    s_company_name     String DEFAULT NULL,
    s_street_number    String DEFAULT NULL,
    s_street_name      String DEFAULT NULL,
    s_street_type      String DEFAULT NULL,
    s_suite_number     String DEFAULT NULL,
    s_city             String DEFAULT NULL,
    s_county           String DEFAULT NULL,
    s_state            String DEFAULT NULL,
    s_zip              String DEFAULT NULL,
    s_country          String DEFAULT NULL,
    s_gmt_offset       Float  DEFAULT NULL,
    s_tax_precentage   Float  DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY s_store_sk;

CREATE TABLE tpcds.call_center
(
    cc_call_center_sk Int32  NOT NULL,
    cc_call_center_id String NOT NULL,
    cc_rec_start_date Date   DEFAULT NULL,
    cc_rec_end_date   Date   DEFAULT NULL,
    cc_closed_date_sk Int32  DEFAULT NULL,
    cc_open_date_sk   Int32  DEFAULT NULL,
    cc_name           String DEFAULT NULL,
    cc_class          String DEFAULT NULL,
    cc_employees      Int32  DEFAULT NULL,
    cc_sq_ft          Int32  DEFAULT NULL,
    cc_hours          String DEFAULT NULL,
    cc_manager        String DEFAULT NULL,
    cc_mkt_id         Int32  DEFAULT NULL,
    cc_mkt_class      String DEFAULT NULL,
    cc_mkt_desc       String DEFAULT NULL,
    cc_market_manager String DEFAULT NULL,
    cc_division       Int32  DEFAULT NULL,
    cc_division_name  String DEFAULT NULL,
    cc_company        Int32  DEFAULT NULL,
    cc_company_name   String DEFAULT NULL,
    cc_street_number  String DEFAULT NULL,
    cc_street_name    String DEFAULT NULL,
    cc_street_type    String DEFAULT NULL,
    cc_suite_number   String DEFAULT NULL,
    cc_city           String DEFAULT NULL,
    cc_county         String DEFAULT NULL,
    cc_state          String DEFAULT NULL,
    cc_zip            String DEFAULT NULL,
    cc_country        String DEFAULT NULL,
    cc_gmt_offset     Float  DEFAULT NULL,
    cc_tax_percentage Float  DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY cc_call_center_sk
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.customer
(
    c_customer_sk          Int32  NOT NULL,
    c_customer_id          String NOT NULL,
    c_current_cdemo_sk     Int32  DEFAULT NULL,
    c_current_hdemo_sk     Int32  DEFAULT NULL,
    c_current_addr_sk      Int32  DEFAULT NULL,
    c_first_shipto_date_sk Int32  DEFAULT NULL,
    c_first_sales_date_sk  Int32  DEFAULT NULL,
    c_salutation           String DEFAULT NULL,
    c_first_name           String DEFAULT NULL,
    c_last_name            String DEFAULT NULL,
    c_preferred_cust_flag  String DEFAULT NULL,
    c_birth_day            Int32  DEFAULT NULL,
    c_birth_month          Int32  DEFAULT NULL,
    c_birth_year           Int32  DEFAULT NULL,
    c_birth_country        String DEFAULT NULL,
    c_login                String DEFAULT NULL,
    c_email_address        String DEFAULT NULL,
    c_last_review_date     Int32  DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY c_customer_sk;

CREATE TABLE tpcds.web_site
(
    web_site_sk        Int32  NOT NULL,
    web_site_id        String NOT NULL,
    web_rec_start_date Date   DEFAULT NULL,
    web_rec_end_date   Date   DEFAULT NULL,
    web_name           String DEFAULT NULL,
    web_open_date_sk   Int32  DEFAULT NULL,
    web_close_date_sk  Int32  DEFAULT NULL,
    web_class          String DEFAULT NULL,
    web_manager        String DEFAULT NULL,
    web_mkt_id         Int32  DEFAULT NULL,
    web_mkt_class      String DEFAULT NULL,
    web_mkt_desc       String DEFAULT NULL,
    web_market_manager String DEFAULT NULL,
    web_company_id     Int32  DEFAULT NULL,
    web_company_name   String DEFAULT NULL,
    web_street_number  String DEFAULT NULL,
    web_street_name    String DEFAULT NULL,
    web_street_type    String DEFAULT NULL,
    web_suite_number   String DEFAULT NULL,
    web_city           String DEFAULT NULL,
    web_county         String DEFAULT NULL,
    web_state          String DEFAULT NULL,
    web_zip            String DEFAULT NULL,
    web_country        String DEFAULT NULL,
    web_gmt_offset     Float  DEFAULT NULL,
    web_tax_percentage Float  DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY web_site_sk;

CREATE TABLE tpcds.store_returns
(
    sr_returned_date_sk   Int32 DEFAULT NULL,
    sr_return_time_sk     Int32 DEFAULT NULL,
    sr_item_sk            Int32 NOT NULL,
    sr_customer_sk        Int32 DEFAULT NULL,
    sr_cdemo_sk           Int32 DEFAULT NULL,
    sr_hdemo_sk           Int32 DEFAULT NULL,
    sr_addr_sk            Int32 DEFAULT NULL,
    sr_store_sk           Int32 DEFAULT NULL,
    sr_reason_sk          Int32 DEFAULT NULL,
    sr_ticket_number      Int32 NOT NULL,
    sr_return_quantity    Int32 DEFAULT NULL,
    sr_return_amt         Float DEFAULT NULL,
    sr_return_tax         Float DEFAULT NULL,
    sr_return_amt_inc_tax Float DEFAULT NULL,
    sr_fee                Float DEFAULT NULL,
    sr_return_ship_cost   Float DEFAULT NULL,
    sr_refunded_cash      Float DEFAULT NULL,
    sr_reversed_charge    Float DEFAULT NULL,
    sr_store_credit       Float DEFAULT NULL,
    sr_net_loss           Float DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY (sr_item_sk, sr_ticket_number);

CREATE TABLE tpcds.household_demographics
(
    hd_demo_sk        Int32  NOT NULL,
    hd_income_band_sk Int32  DEFAULT NULL,
    hd_buy_potential  String DEFAULT NULL,
    hd_dep_count      Int32  DEFAULT NULL,
    hd_vehicle_count  Int32  DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY hd_demo_sk
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.web_page
(
    wp_web_page_sk      Int32  NOT NULL,
    wp_web_page_id      String NOT NULL,
    wp_rec_start_date   Date   DEFAULT NULL,
    wp_rec_end_date     Date   DEFAULT NULL,
    wp_creation_date_sk Int32  DEFAULT NULL,
    wp_access_date_sk   Int32  DEFAULT NULL,
    wp_autogen_flag     String DEFAULT NULL,
    wp_customer_sk      Int32  DEFAULT NULL,
    wp_url              String DEFAULT NULL,
    wp_type             String DEFAULT NULL,
    wp_char_count       Int32  DEFAULT NULL,
    wp_link_count       Int32  DEFAULT NULL,
    wp_image_count      Int32  DEFAULT NULL,
    wp_max_ad_count     Int32  DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY wp_web_page_sk;

CREATE TABLE tpcds.promotion
(
    p_promo_sk        Int32  NOT NULL,
    p_promo_id        String NOT NULL,
    p_start_date_sk   Int32  DEFAULT NULL,
    p_end_date_sk     Int32  DEFAULT NULL,
    p_item_sk         Int32  DEFAULT NULL,
    p_cost            Float  DEFAULT NULL,
    p_response_target Int32  DEFAULT NULL,
    p_promo_name      String DEFAULT NULL,
    p_channel_dmail   String DEFAULT NULL,
    p_channel_email   String DEFAULT NULL,
    p_channel_catalog String DEFAULT NULL,
    p_channel_tv      String DEFAULT NULL,
    p_channel_radio   String DEFAULT NULL,
    p_channel_press   String DEFAULT NULL,
    p_channel_event   String DEFAULT NULL,
    p_channel_demo    String DEFAULT NULL,
    p_channel_details String DEFAULT NULL,
    p_purpose         String DEFAULT NULL,
    p_discount_active String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY p_promo_sk;

CREATE TABLE tpcds.catalog_page
(
    cp_catalog_page_sk     Int32  NOT NULL,
    cp_catalog_page_id     String NOT NULL,
    cp_start_date_sk       Int32  DEFAULT NULL,
    cp_end_date_sk         Int32  DEFAULT NULL,
    cp_department          String DEFAULT NULL,
    cp_catalog_number      Int32  DEFAULT NULL,
    cp_catalog_page_number Int32  DEFAULT NULL,
    cp_description         String DEFAULT NULL,
    cp_type                String DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY cp_catalog_page_sk;

CREATE TABLE tpcds.inventory
(
    inv_date_sk          Int32 NOT NULL,
    inv_item_sk          Int32 NOT NULL,
    inv_warehouse_sk     Int32 NOT NULL,
    inv_quantity_on_hand Int32 DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY (inv_date_sk, inv_item_sk, inv_warehouse_sk)
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.catalog_returns
(
    cr_returned_date_sk      Int32 DEFAULT NULL,
    cr_returned_time_sk      Int32 DEFAULT NULL,
    cr_item_sk               Int32 NOT NULL,
    cr_refunded_customer_sk  Int32 DEFAULT NULL,
    cr_refunded_cdemo_sk     Int32 DEFAULT NULL,
    cr_refunded_hdemo_sk     Int32 DEFAULT NULL,
    cr_refunded_addr_sk      Int32 DEFAULT NULL,
    cr_returning_customer_sk Int32 DEFAULT NULL,
    cr_returning_cdemo_sk    Int32 DEFAULT NULL,
    cr_returning_hdemo_sk    Int32 DEFAULT NULL,
    cr_returning_addr_sk     Int32 DEFAULT NULL,
    cr_call_center_sk        Int32 DEFAULT NULL,
    cr_catalog_page_sk       Int32 DEFAULT NULL,
    cr_ship_mode_sk          Int32 DEFAULT NULL,
    cr_warehouse_sk          Int32 DEFAULT NULL,
    cr_reason_sk             Int32 DEFAULT NULL,
    cr_order_number          Int32 NOT NULL,
    cr_return_quantity       Int32 DEFAULT NULL,
    cr_return_amount         Float DEFAULT NULL,
    cr_return_tax            Float DEFAULT NULL,
    cr_return_amt_inc_tax    Float DEFAULT NULL,
    cr_fee                   Float DEFAULT NULL,
    cr_return_ship_cost      Float DEFAULT NULL,
    cr_refunded_cash         Float DEFAULT NULL,
    cr_reversed_charge       Float DEFAULT NULL,
    cr_store_credit          Float DEFAULT NULL,
    cr_net_loss              Float DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY (cr_item_sk, cr_order_number);

CREATE TABLE tpcds.web_returns
(
    wr_returned_date_sk      Int32 DEFAULT NULL,
    wr_returned_time_sk      Int32 DEFAULT NULL,
    wr_item_sk               Int32 NOT NULL,
    wr_refunded_customer_sk  Int32 DEFAULT NULL,
    wr_refunded_cdemo_sk     Int32 DEFAULT NULL,
    wr_refunded_hdemo_sk     Int32 DEFAULT NULL,
    wr_refunded_addr_sk      Int32 DEFAULT NULL,
    wr_returning_customer_sk Int32 DEFAULT NULL,
    wr_returning_cdemo_sk    Int32 DEFAULT NULL,
    wr_returning_hdemo_sk    Int32 DEFAULT NULL,
    wr_returning_addr_sk     Int32 DEFAULT NULL,
    wr_web_page_sk           Int32 DEFAULT NULL,
    wr_reason_sk             Int32 DEFAULT NULL,
    wr_order_number          Int32 NOT NULL,
    wr_return_quantity       Int32 DEFAULT NULL,
    wr_return_amt            Float DEFAULT NULL,
    wr_return_tax            Float DEFAULT NULL,
    wr_return_amt_inc_tax    Float DEFAULT NULL,
    wr_fee                   Float DEFAULT NULL,
    wr_return_ship_cost      Float DEFAULT NULL,
    wr_refunded_cash         Float DEFAULT NULL,
    wr_reversed_charge       Float DEFAULT NULL,
    wr_account_credit        Float DEFAULT NULL,
    wr_net_loss              Float DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY (wr_item_sk, wr_order_number);

CREATE TABLE tpcds.web_sales
(
    ws_sold_date_sk          Int32 DEFAULT NULL,
    ws_sold_time_sk          Int32 DEFAULT NULL,
    ws_ship_date_sk          Int32 DEFAULT NULL,
    ws_item_sk               Int32 NOT NULL,
    ws_bill_customer_sk      Int32 DEFAULT NULL,
    ws_bill_cdemo_sk         Int32 DEFAULT NULL,
    ws_bill_hdemo_sk         Int32 DEFAULT NULL,
    ws_bill_addr_sk          Int32 DEFAULT NULL,
    ws_ship_customer_sk      Int32 DEFAULT NULL,
    ws_ship_cdemo_sk         Int32 DEFAULT NULL,
    ws_ship_hdemo_sk         Int32 DEFAULT NULL,
    ws_ship_addr_sk          Int32 DEFAULT NULL,
    ws_web_page_sk           Int32 DEFAULT NULL,
    ws_web_site_sk           Int32 DEFAULT NULL,
    ws_ship_mode_sk          Int32 DEFAULT NULL,
    ws_warehouse_sk          Int32 DEFAULT NULL,
    ws_promo_sk              Int32 DEFAULT NULL,
    ws_order_number          Int32 NOT NULL,
    ws_quantity              Int32 DEFAULT NULL,
    ws_wholesale_cost        Float DEFAULT NULL,
    ws_list_price            Float DEFAULT NULL,
    ws_sales_price           Float DEFAULT NULL,
    ws_ext_discount_amt      Float DEFAULT NULL,
    ws_ext_sales_price       Float DEFAULT NULL,
    ws_ext_wholesale_cost    Float DEFAULT NULL,
    ws_ext_list_price        Float DEFAULT NULL,
    ws_ext_tax               Float DEFAULT NULL,
    ws_coupon_amt            Float DEFAULT NULL,
    ws_ext_ship_cost         Float DEFAULT NULL,
    ws_net_paid              Float DEFAULT NULL,
    ws_net_paid_inc_tax      Float DEFAULT NULL,
    ws_net_paid_inc_ship     Float DEFAULT NULL,
    ws_net_paid_inc_ship_tax Float DEFAULT NULL,
    ws_net_profit            Float DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY (ws_item_sk, ws_order_number)
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.catalog_sales
(
    cs_sold_date_sk          Int32 DEFAULT NULL,
    cs_sold_time_sk          Int32 DEFAULT NULL,
    cs_ship_date_sk          Int32 DEFAULT NULL,
    cs_bill_customer_sk      Int32 DEFAULT NULL,
    cs_bill_cdemo_sk         Int32 DEFAULT NULL,
    cs_bill_hdemo_sk         Int32 DEFAULT NULL,
    cs_bill_addr_sk          Int32 DEFAULT NULL,
    cs_ship_customer_sk      Int32 DEFAULT NULL,
    cs_ship_cdemo_sk         Int32 DEFAULT NULL,
    cs_ship_hdemo_sk         Int32 DEFAULT NULL,
    cs_ship_addr_sk          Int32 DEFAULT NULL,
    cs_call_center_sk        Int32 DEFAULT NULL,
    cs_catalog_page_sk       Int32 DEFAULT NULL,
    cs_ship_mode_sk          Int32 DEFAULT NULL,
    cs_warehouse_sk          Int32 DEFAULT NULL,
    cs_item_sk               Int32 NOT NULL,
    cs_promo_sk              Int32 DEFAULT NULL,
    cs_order_number          Int32 NOT NULL,
    cs_quantity              Int32 DEFAULT NULL,
    cs_wholesale_cost        Float DEFAULT NULL,
    cs_list_price            Float DEFAULT NULL,
    cs_sales_price           Float DEFAULT NULL,
    cs_ext_discount_amt      Float DEFAULT NULL,
    cs_ext_sales_price       Float DEFAULT NULL,
    cs_ext_wholesale_cost    Float DEFAULT NULL,
    cs_ext_list_price        Float DEFAULT NULL,
    cs_ext_tax               Float DEFAULT NULL,
    cs_coupon_amt            Float DEFAULT NULL,
    cs_ext_ship_cost         Float DEFAULT NULL,
    cs_net_paid              Float DEFAULT NULL,
    cs_net_paid_inc_tax      Float DEFAULT NULL,
    cs_net_paid_inc_ship     Float DEFAULT NULL,
    cs_net_paid_inc_ship_tax Float DEFAULT NULL,
    cs_net_profit            Float DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY (cs_item_sk, cs_order_number);

CREATE TABLE tpcds.store_sales
(
    ss_sold_date_sk       Int32 DEFAULT NULL,
    ss_sold_time_sk       Int32 DEFAULT NULL,
    ss_item_sk            Int32 NOT NULL,
    ss_customer_sk        Int32 DEFAULT NULL,
    ss_cdemo_sk           Int32 DEFAULT NULL,
    ss_hdemo_sk           Int32 DEFAULT NULL,
    ss_addr_sk            Int32 DEFAULT NULL,
    ss_store_sk           Int32 DEFAULT NULL,
    ss_promo_sk           Int32 DEFAULT NULL,
    ss_ticket_number      Int32 NOT NULL,
    ss_quantity           Int32 DEFAULT NULL,
    ss_wholesale_cost     Float DEFAULT NULL,
    ss_list_price         Float DEFAULT NULL,
    ss_sales_price        Float DEFAULT NULL,
    ss_ext_discount_amt   Float DEFAULT NULL,
    ss_ext_sales_price    Float DEFAULT NULL,
    ss_ext_wholesale_cost Float DEFAULT NULL,
    ss_ext_list_price     Float DEFAULT NULL,
    ss_ext_tax            Float DEFAULT NULL,
    ss_coupon_amt         Float DEFAULT NULL,
    ss_net_paid           Float DEFAULT NULL,
    ss_net_paid_inc_tax   Float DEFAULT NULL,
    ss_net_profit         Float DEFAULT NULL
)
ENGINE = MergeTree()
ORDER BY (ss_item_sk, ss_ticket_number);
