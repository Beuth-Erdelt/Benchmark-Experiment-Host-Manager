create database tpcds;


SET data_type_default_nullable=1;
SET cast_keep_nullable = 1;

SELECT *　FROM system.settings　WHERE name LIKE '%null%';

CREATE TABLE tpcds.customer_address
(
    `ca_address_sk` Int32 not null, 
    `ca_address_id` String not null, 
    `ca_street_number` String default null, 
    `ca_street_name` String default null, 
    `ca_street_type` String default null, 
    `ca_suite_number` String default null, 
    `ca_city` String default null, 
    `ca_county` String default null, 
    `ca_state` String default null, 
    `ca_zip` String default null, 
    `ca_country` String default null, 
    `ca_gmt_offset` Float default null, 
    `ca_location_type` String default null
)
ENGINE = MergeTree()
ORDER BY ca_address_sk
SETTINGS index_granularity = 8192;
---------------------------------------------------------------------------------

---------------------------------------------------------------------------------


CREATE TABLE tpcds.customer_demographics
(
    `cd_demo_sk` Int32 not null, 
    `cd_gender` String default null, 
    `cd_marital_status` String default null, 
    `cd_education_status` String default null, 
    `cd_purchase_estimate` Int32 default null, 
    `cd_credit_rating` String default null, 
    `cd_dep_count` Int32 default null, 
    `cd_dep_employed_count` Int32 default null, 
    `cd_dep_college_count` Int32 default null
)
ENGINE = MergeTree()
ORDER BY cd_demo_sk
SETTINGS index_granularity = 8192;

---------------------------------------------------------------------------------


CREATE TABLE tpcds.warehouse
(
    `w_warehouse_sk` Int32 not null, 
    `w_warehouse_id` String default null, 
    `w_warehouse_name` String default null, 
    `w_warehouse_sq_ft` int default null, 
    `w_street_number` String default null, 
    `w_street_name` String default null, 
    `w_street_type` String default null, 
    `w_suite_number` String default null, 
    `w_city` String default null, 
    `w_county` String default null, 
    `w_state` String default null, 
    `w_zip` String default null, 
    `w_country` String default null, 
    `w_gmt_offset` Float default null
)
ENGINE = MergeTree()
ORDER BY w_warehouse_sk;



CREATE TABLE tpcds.ship_mode
(
    `sm_ship_mode_sk` Int32 not null, 
    `sm_ship_mode_id` String not null, 
    `sm_type` String default null, 
    `sm_code` String default null, 
    `sm_carrier` String default null, 
    `sm_contract` String default null
)
ENGINE = MergeTree()
ORDER BY sm_ship_mode_sk
SETTINGS index_granularity = 8192;





CREATE TABLE tpcds.time_dim
(
    `t_time_sk` Int32 not null, 
    `t_time_id` String not null, 
    `t_time` Int32 not null, 
    `t_hour` Int32 default null, 
    `t_minute` Int32 default null, 
    `t_second` Int32 default null, 
    `t_am_pm` String default null, 
    `t_shift` String default null, 
    `t_sub_shift` String default null, 
    `t_meal_time` String default null
)
ENGINE = MergeTree()
ORDER BY (t_time_sk);



CREATE TABLE tpcds.reason
(
    `r_reason_sk` Int32 not null, 
    `r_reason_id` String not null, 
    `r_reason_desc` String default null
)
ENGINE = MergeTree()
ORDER BY r_reason_sk
SETTINGS index_granularity = 8192;


CREATE TABLE tpcds.income_band
(
    `ib_income_band_sk` Int32 not null, 
    `ib_lower_bound` Int32 default null, 
    `ib_upper_bound` Int32 default null
)
ENGINE = MergeTree()
ORDER BY ib_income_band_sk
SETTINGS index_granularity = 8192;



CREATE TABLE tpcds.catalog_sales (
`cs_sold_date_sk` Int32 default null, 
`cs_sold_time_sk` Int32 default null,
`cs_ship_date_sk` Int32 default null, 
`cs_bill_customer_sk` Int32 default null, 
`cs_bill_cdemo_sk` Int32 default null, 
`cs_bill_hdemo_sk` Int32 default null, 
`cs_bill_addr_sk` Int32 default null,    
`cs_ship_customer_sk` Int32 default null, 
`cs_ship_cdemo_sk` Int32 default null,     
`cs_ship_hdemo_sk` Int32 default null,   
`cs_ship_addr_sk` Int32 default null, 
`cs_call_center_sk` Int32 default null,
`cs_catalog_page_sk` Int32 default null, 
`cs_ship_mode_sk` Int32 default null,
`cs_warehouse_sk` Int32 default null, 
`cs_item_sk` Int32 not null,
`cs_promo_sk` Int32 default null, 
`cs_order_number` Int32 not null, 
`cs_quantity` Int32 default null, 
`cs_wholesale_cost` Float default null,
`cs_list_price` Float default null, 
`cs_sales_price` Float default null, 
`cs_ext_discount_amt` Float default null,
`cs_ext_sales_price` Float default null,
`cs_ext_wholesale_cost` Float default null, 
`cs_ext_list_price` Float default null, 
`cs_ext_tax` Float default null,
`cs_coupon_amt` Float default null, 
`cs_ext_ship_cost` Float default null, 
`cs_net_paid` Float default null,
`cs_net_paid_inc_tax` Float default null, 
`cs_net_paid_inc_ship` Float default null,
`cs_net_paid_inc_ship_tax` Float default null, 
`cs_net_profit` Float default null
) 
ENGINE = MergeTree() ORDER BY (cs_item_sk, cs_order_number);

CREATE TABLE tpcds.call_center 
(
`cc_call_center_sk` Int32 not null, 
`cc_call_center_id` String not null,
`cc_rec_start_date` Date default null, 
`cc_rec_end_date` Date default null, 
`cc_closed_date_sk` Int32 default null,
`cc_open_date_sk` Int32 default null, 
`cc_name` String default null, 
`cc_class` String default null, 
`cc_employees` Int32 default null, 
`cc_sq_ft` Int32 default null, 
`cc_hours` String default null,
`cc_manager` String default null,
`cc_mkt_id` Int32 default null,
`cc_mkt_class` String default null, 
`cc_mkt_desc` String default null, 
`cc_market_manager` String default null, 
`cc_division` Int32 default null, 
`cc_division_name` String default null,
`cc_company` Int32 default null, 
`cc_company_name` String default null, 
`cc_street_number` String default null,
`cc_street_name` String default null, 
`cc_street_type` String default null, 
`cc_suite_number` String default null,
`cc_city` String default null, 
`cc_county` String default null, 
`cc_state` String default null, 
`cc_zip` String default null, 
`cc_country` String default null, 
`cc_gmt_offset` Float default null,
`cc_tax_percentage` Float default null
) 
ENGINE = MergeTree()
ORDER BY cc_call_center_sk
SETTINGS index_granularity = 8192;


CREATE TABLE tpcds.date_dim
(
    d_date_sk Int32 not null, 
    d_date_id String not null, 
    d_date Date not null, 
    d_month_seq Int32 default null, 
    d_week_seq Int32 default null, 
    d_quarter_seq Int32 default null, 
    d_year Int32 default null, 
    d_dow Int32 default null, 
    d_moy Int32 default null, 
    d_dom Int32 default null, 
    d_qoy Int32 default null, 
    d_fy_year Int32 default null, 
    d_fy_quarter_seq Int32 default null, 
    d_fy_week_seq Int32 default null, 
    d_day_name String default null, 
    d_quarter_name String default null, 
    d_holiday String default null, 
    d_weekend String default null, 
    d_following_holiday String default null, 
    d_first_dom Int32 default null, 
    d_last_dom Int32 default null, 
    d_same_day_ly Int32 default null, 
    d_same_day_lq Int32 default null, 
    d_current_day String default null, 
    d_current_week String default null, 
    d_current_month String default null, 
    d_current_quarter String default null, 
    d_current_year String default null
)
ENGINE = MergeTree()
ORDER BY (d_date_sk);


CREATE TABLE tpcds.household_demographics
(
    `hd_demo_sk` Int32 not null, 
    `hd_income_band_sk` Int32 default null, 
    `hd_buy_potential` String default null, 
    `hd_dep_count` Int32 default null, 
    `hd_vehicle_count` Int32 default null
)
ENGINE = MergeTree()
ORDER BY hd_demo_sk
SETTINGS index_granularity = 8192;

CREATE TABLE tpcds.item
(
    `i_item_sk` Int32 not null, 
    `i_item_id` String not null, 
    `i_rec_start_date` Date default null, 
    `i_rec_end_date` Date default null, 
    `i_item_desc` String default null, 
    `i_current_price` Float default null, 
    `i_wholesale_cost` Float default null, 
    `i_brand_id` Int32 default null, 
    `i_brand` String default null, 
    `i_class_id` Int32 default null, 
    `i_class` String default null, 
    `i_category_id` Int32 default null, 
    `i_category` String default null, 
    `i_manufact_id` Int32 default null, 
    `i_manufact` String default null, 
    `i_size` String default null, 
    `i_formulation` String default null, 
    `i_color` String default null, 
    `i_units` String default null, 
    `i_container` String default null, 
    `i_manager_id` Int32 default null, 
    `i_product_name` String default null
)
ENGINE = MergeTree()
ORDER BY (i_item_sk);



CREATE TABLE tpcds.store (
        s_store_sk Int32 not null,
        s_store_id String not null,
        s_rec_start_date Date default null,
        s_rec_end_date Date default null,
        s_closed_date_sk Int32 default null,
        s_store_name String default null,
        s_number_employees Int32 default null,
        s_floor_space Int32 default null,
        s_hours String default null,
        s_manager String default null,
        s_market_id Int32 default null,
        s_geography_class String default null,
        s_market_desc String default null,
        s_market_manager String default null,
        s_division_id Int32 default null,
        s_division_name String default null,
        s_company_id Int32 default null,
        s_company_name String default null,
        s_street_number String default null,
        s_street_name String default null,
        s_street_type String default null,
        s_suite_number String default null,
        s_city String default null,
        s_county String default null,
        s_state String default null,
        s_zip String default null,
        s_country String default null,
        s_gmt_offset Float default null,
        s_tax_precentage Float default null
)
ENGINE = MergeTree()
ORDER BY s_store_sk;


CREATE TABLE tpcds.customer
(
    `c_customer_sk` Int32 not null, 
    `c_customer_id` String not null, 
    `c_current_cdemo_sk` Int32 default null, 
    `c_current_hdemo_sk` Int32 default null, 
    `c_current_addr_sk` Int32 default null, 
    `c_first_shipto_date_sk` Int32 default null, 
    `c_first_sales_date_sk` Int32 default null, 
    `c_salutation` String default null, 
    `c_first_name` String default null, 
    `c_last_name` String default null, 
    `c_preferred_cust_flag` String default null, 
    `c_birth_day` Int32 default null, 
    `c_birth_month` Int32 default null, 
    `c_birth_year` Int32 default null, 
    `c_birth_country` String default null, 
    `c_login` String default null, 
    `c_email_address` String default null, 
    `c_last_review_date` Int32 default null
)
ENGINE = MergeTree()
ORDER BY c_customer_sk;


CREATE TABLE tpcds.store_sales (
    ss_sold_date_sk Int32 default null,
    ss_sold_time_sk Int32 default null,
    ss_item_sk Int32  not null,
    ss_customer_sk Int32 default null,
    ss_cdemo_sk Int32 default null,
    ss_hdemo_sk Int32 default null,
    ss_addr_sk Int32 default null,
    ss_store_sk Int32 default null,
    ss_promo_sk Int32 default null,
    ss_ticket_number Int32  not null,
    ss_quantity Int32 default null,
    ss_wholesale_cost Float default null,
    ss_list_price Float default null,
    ss_sales_price Float default null,
    ss_ext_discount_amt Float default null,
    ss_ext_sales_price Float default null,
    ss_ext_wholesale_cost Float default null,
    ss_ext_list_price Float default null,
    ss_ext_tax Float default null,
    ss_coupon_amt Float default null,
    ss_net_paid Float default null,
    ss_net_paid_inc_tax Float default null,
    ss_net_profit Float default null
)
ENGINE = MergeTree()
ORDER BY (ss_item_sk, ss_ticket_number);



CREATE TABLE tpcds.web_sales (
    ws_sold_date_sk Int32 default null,
    ws_sold_time_sk Int32 default null,
    ws_ship_date_sk Int32 default null,
    ws_item_sk Int32  not null,
    ws_bill_customer_sk Int32 default null,
    ws_bill_cdemo_sk Int32 default null,
    ws_bill_hdemo_sk Int32 default null,
    ws_bill_addr_sk Int32 default null,
    ws_ship_customer_sk Int32 default null,
    ws_ship_cdemo_sk Int32 default null,
    ws_ship_hdemo_sk Int32 default null,
    ws_ship_addr_sk Int32 default null,
    ws_web_page_sk Int32 default null,
    ws_web_site_sk Int32 default null,
    ws_ship_mode_sk Int32 default null,
    ws_warehouse_sk Int32 default null,
    ws_promo_sk Int32 default null,
    ws_order_number Int32  not null,
    ws_quantity Int32 default null,
    ws_wholesale_cost Float default null,
    ws_list_price Float default null,
    ws_sales_price Float default null,
    ws_ext_discount_amt Float default null,
    ws_ext_sales_price Float default null,
    ws_ext_wholesale_cost Float default null,
    ws_ext_list_price Float default null,
    ws_ext_tax Float default null,
    ws_coupon_amt Float default null,
    ws_ext_ship_cost Float default null,
    ws_net_paid Float default null,
    ws_net_paid_inc_tax Float default null,
    ws_net_paid_inc_ship Float default null,
    ws_net_paid_inc_ship_tax Float default null,
    ws_net_profit Float default null
)
ENGINE = MergeTree()
ORDER BY (ws_item_sk, ws_order_number)
SETTINGS index_granularity = 8192 ;



create table tpcds.dbgen_version
(
    dv_version                String default null,
    dv_create_date            Date                          ,
    dv_create_time            String                        ,
    dv_cmdline_args           String                  
)
ENGINE = MergeTree()
ORDER BY tuple()
SETTINGS index_granularity = 8192 ;



create table tpcds.catalog_page
(
    cp_catalog_page_sk        Int32  not null,
    cp_catalog_page_id        String not null,
    cp_start_date_sk          Int32 default null,
    cp_end_date_sk            Int32 default null,
    cp_department             String default null,
    cp_catalog_number         Int32 default null,
    cp_catalog_page_number    Int32 default null,
    cp_description            String default null,
    cp_type                   String default null
)
ENGINE = MergeTree()
ORDER BY (cp_catalog_page_sk);



create table tpcds.catalog_returns
(
    cr_returned_date_sk       Int32 default null,
    cr_returned_time_sk       Int32 default null,
    cr_item_sk                Int32 not null,
    cr_refunded_customer_sk   Int32 default null,
    cr_refunded_cdemo_sk      Int32 default null,
    cr_refunded_hdemo_sk      Int32 default null,
    cr_refunded_addr_sk       Int32 default null,
    cr_returning_customer_sk  Int32 default null,
    cr_returning_cdemo_sk     Int32 default null,
    cr_returning_hdemo_sk     Int32 default null,
    cr_returning_addr_sk      Int32 default null,
    cr_call_center_sk         Int32 default null,
    cr_catalog_page_sk        Int32 default null,
    cr_ship_mode_sk           Int32 default null,
    cr_warehouse_sk           Int32 default null,
    cr_reason_sk              Int32 default null,
    cr_order_number           Int32 not null,
    cr_return_quantity        Int32 default null,
    cr_return_amount          Float default null,
    cr_return_tax             Float default null,
    cr_return_amt_inc_tax     Float default null,
    cr_fee                    Float default null,
    cr_return_ship_cost       Float default null,
    cr_refunded_cash          Float default null,
    cr_reversed_charge        Float default null,
    cr_store_credit           Float default null,
    cr_net_loss               Float default null
)
ENGINE = MergeTree()
ORDER BY (cr_item_sk, cr_order_number);



create table tpcds.inventory
(
    inv_date_sk               Int32 not null,
    inv_item_sk               Int32 not null,
    inv_warehouse_sk          Int32 not null,
    inv_quantity_on_hand      Int32 default null
)
ENGINE = MergeTree()
ORDER BY (inv_date_sk, inv_item_sk, inv_warehouse_sk)
SETTINGS index_granularity = 8192 ;



create table tpcds.promotion
(
    p_promo_sk                Int32 not null,
    p_promo_id                String not null,
    p_start_date_sk           Int32 default null,
    p_end_date_sk             Int32 default null,
    p_item_sk                 Int32 default null,
    p_cost                    Float default null,
    p_response_target         Int32 default null,
    p_promo_name              String default null,
    p_channel_dmail           String default null,
    p_channel_email           String default null,
    p_channel_catalog         String default null,
    p_channel_tv              String default null,
    p_channel_radio           String default null,
    p_channel_press           String default null,
    p_channel_event           String default null,
    p_channel_demo            String default null,
    p_channel_details         String default null,
    p_purpose                 String default null,
    p_discount_active         String default null                     
)
ENGINE = MergeTree()
ORDER BY p_promo_sk;


create table tpcds.store_returns
(
    sr_returned_date_sk       Int32 default null,
    sr_return_time_sk         Int32 default null,
    sr_item_sk                Int32 not null,
    sr_customer_sk            Int32 default null,
    sr_cdemo_sk               Int32 default null,
    sr_hdemo_sk               Int32 default null,
    sr_addr_sk                Int32 default null,
    sr_store_sk               Int32 default null,
    sr_reason_sk              Int32 default null,
    sr_ticket_number          Int32 not null,
    sr_return_quantity        Int32 default null,
    sr_return_amt             Float default null,
    sr_return_tax             Float default null,
    sr_return_amt_inc_tax     Float default null,
    sr_fee                    Float default null,
    sr_return_ship_cost       Float default null,
    sr_refunded_cash          Float default null,
    sr_reversed_charge        Float default null,
    sr_store_credit           Float default null,
    sr_net_loss               Float default null
)
ENGINE = MergeTree()
ORDER BY (sr_item_sk, sr_ticket_number);



create table tpcds.web_page
(
    wp_web_page_sk            Int32 not null,
    wp_web_page_id            String not null,
    wp_rec_start_date         Date default null,
    wp_rec_end_date           Date default null,
    wp_creation_date_sk       Int32 default null,
    wp_access_date_sk         Int32 default null,
    wp_autogen_flag           String default null,
    wp_customer_sk            Int32 default null,
    wp_url                    String default null,
    wp_type                   String default null,
    wp_char_count             Int32 default null,
    wp_link_count             Int32 default null,
    wp_image_count            Int32 default null,
    wp_max_ad_count           Int32 default null
)
ENGINE = MergeTree()
ORDER BY wp_web_page_sk;



create table tpcds.web_returns
(
    wr_returned_date_sk       Int32 default null,
    wr_returned_time_sk       Int32 default null,
    wr_item_sk                Int32               not null,
    wr_refunded_customer_sk   Int32 default null,
    wr_refunded_cdemo_sk      Int32 default null,
    wr_refunded_hdemo_sk      Int32 default null,
    wr_refunded_addr_sk       Int32 default null,
    wr_returning_customer_sk  Int32 default null,
    wr_returning_cdemo_sk     Int32 default null,
    wr_returning_hdemo_sk     Int32 default null,
    wr_returning_addr_sk      Int32 default null,
    wr_web_page_sk            Int32 default null,
    wr_reason_sk              Int32 default null,
    wr_order_number           Int32               not null,
    wr_return_quantity        Int32 default null,
    wr_return_amt             Float default null,
    wr_return_tax             Float default null,
    wr_return_amt_inc_tax     Float default null,
    wr_fee                    Float default null,
    wr_return_ship_cost       Float default null,
    wr_refunded_cash          Float default null,
    wr_reversed_charge        Float default null,
    wr_account_credit         Float default null,
    wr_net_loss               Float default null
)
ENGINE = MergeTree()
ORDER BY (wr_item_sk, wr_order_number);



create table tpcds.web_site
(
    web_site_sk               Int32               not null,
    web_site_id               String              not null,
    web_rec_start_date        Date default null,
    web_rec_end_date          Date default null,
    web_name                  String default null,
    web_open_date_sk          Int32 default null,
    web_close_date_sk         Int32 default null,
    web_class                 String default null,
    web_manager               String default null,
    web_mkt_id                Int32 default null,
    web_mkt_class             String default null,
    web_mkt_desc              String default null,
    web_market_manager        String default null,
    web_company_id            Int32 default null,
    web_company_name          String default null,
    web_street_number         String default null,
    web_street_name           String default null,
    web_street_type           String default null,
    web_suite_number          String default null,
    web_city                  String default null,
    web_county                String default null,
    web_state                 String default null,
    web_zip                   String default null,
    web_country               String default null,
    web_gmt_offset            Float default null,
    web_tax_percentage        Float default null
)
ENGINE = MergeTree()
ORDER BY (web_site_sk);

