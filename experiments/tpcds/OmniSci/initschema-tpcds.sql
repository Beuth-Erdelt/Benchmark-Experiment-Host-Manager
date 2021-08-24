
create table dbgen_version
(
    dv_version                TEXT ENCODING DICT                   ,
    dv_create_date            date                          ,
    dv_create_time            time                          ,
    dv_cmdline_args           TEXT ENCODING DICT                  
);

create table customer_address
(
    ca_address_sk             integer               not null,
    ca_address_id             TEXT NOT NULL ENCODING DICT            ,
    ca_street_number          TEXT ENCODING DICT                      ,
    ca_street_name            TEXT ENCODING DICT                   ,
    ca_street_type            TEXT ENCODING DICT                      ,
    ca_suite_number           TEXT ENCODING DICT                      ,
    ca_city                   TEXT ENCODING DICT                   ,
    ca_county                 TEXT ENCODING DICT                   ,
    ca_state                  TEXT ENCODING DICT                       ,
    ca_zip                    TEXT ENCODING DICT                      ,
    ca_country                TEXT ENCODING DICT                   ,
    ca_gmt_offset             decimal(5,2)                  ,
    ca_location_type          TEXT ENCODING DICT
);

create table customer_demographics
(
    cd_demo_sk                integer               not null,
    cd_gender                 TEXT ENCODING DICT                       ,
    cd_marital_status         TEXT ENCODING DICT                       ,
    cd_education_status       TEXT ENCODING DICT                      ,
    cd_purchase_estimate      integer                       ,
    cd_credit_rating          TEXT ENCODING DICT                      ,
    cd_dep_count              integer                       ,
    cd_dep_employed_count     integer                       ,
    cd_dep_college_count      integer
);

create table date_dim
(
    d_date_sk                 integer               not null,
    d_date_id                 TEXT NOT NULL ENCODING DICT            ,
    d_date                    date                          ,
    d_month_seq               integer                       ,
    d_week_seq                integer                       ,
    d_quarter_seq             integer                       ,
    d_year                    integer                       ,
    d_dow                     integer                       ,
    d_moy                     integer                       ,
    d_dom                     integer                       ,
    d_qoy                     integer                       ,
    d_fy_year                 integer                       ,
    d_fy_quarter_seq          integer                       ,
    d_fy_week_seq             integer                       ,
    d_day_name                TEXT ENCODING DICT                       ,
    d_quarter_name            TEXT ENCODING DICT                       ,
    d_holiday                 TEXT ENCODING DICT                       ,
    d_weekend                 TEXT ENCODING DICT                       ,
    d_following_holiday       TEXT ENCODING DICT                       ,
    d_first_dom               integer                       ,
    d_last_dom                integer                       ,
    d_same_day_ly             integer                       ,
    d_same_day_lq             integer                       ,
    d_current_day             TEXT ENCODING DICT                       ,
    d_current_week            TEXT ENCODING DICT                       ,
    d_current_month           TEXT ENCODING DICT                       ,
    d_current_quarter         TEXT ENCODING DICT                       ,
    d_current_year            TEXT ENCODING DICT
);

create table warehouse
(
    w_warehouse_sk            integer               not null,
    w_warehouse_id            TEXT NOT NULL ENCODING DICT            ,
    w_warehouse_name          TEXT ENCODING DICT                   ,
    w_warehouse_sq_ft         integer                       ,
    w_street_number           TEXT ENCODING DICT                      ,
    w_street_name             TEXT ENCODING DICT                   ,
    w_street_type             TEXT ENCODING DICT                      ,
    w_suite_number            TEXT ENCODING DICT                      ,
    w_city                    TEXT ENCODING DICT                   ,
    w_county                  TEXT ENCODING DICT                   ,
    w_state                   TEXT ENCODING DICT                       ,
    w_zip                     TEXT ENCODING DICT                      ,
    w_country                 TEXT ENCODING DICT                   ,
    w_gmt_offset              decimal(5,2)
);

create table ship_mode
(
    sm_ship_mode_sk           integer               not null,
    sm_ship_mode_id           TEXT NOT NULL ENCODING DICT            ,
    sm_type                   TEXT ENCODING DICT                      ,
    sm_code                   TEXT ENCODING DICT                      ,
    sm_carrier                TEXT ENCODING DICT                      ,
    sm_contract               TEXT ENCODING DICT
);

create table time_dim
(
    t_time_sk                 integer               not null,
    t_time_id                 TEXT NOT NULL ENCODING DICT            ,
    t_time                    integer                       ,
    t_hour                    integer                       ,
    t_minute                  integer                       ,
    t_second                  integer                       ,
    t_am_pm                   TEXT ENCODING DICT                       ,
    t_shift                   TEXT ENCODING DICT                      ,
    t_sub_shift               TEXT ENCODING DICT                      ,
    t_meal_time               TEXT ENCODING DICT
);

create table reason
(
    r_reason_sk               integer               not null,
    r_reason_id               TEXT NOT NULL ENCODING DICT            ,
    r_reason_desc             TEXT ENCODING DICT
);

create table income_band
(
    ib_income_band_sk         integer               not null,
    ib_lower_bound            integer                       ,
    ib_upper_bound            integer
);

create table item
(
    i_item_sk                 integer               not null,
    i_item_id                 TEXT NOT NULL ENCODING DICT            ,
    i_rec_start_date          date                          ,
    i_rec_end_date            date                          ,
    i_item_desc               TEXT ENCODING DICT                  ,
    i_current_price           decimal(7,2)                  ,
    i_wholesale_cost          decimal(7,2)                  ,
    i_brand_id                integer                       ,
    i_brand                   TEXT ENCODING DICT                      ,
    i_class_id                integer                       ,
    i_class                   TEXT ENCODING DICT                      ,
    i_category_id             integer                       ,
    i_category                TEXT ENCODING DICT                      ,
    i_manufact_id             integer                       ,
    i_manufact                TEXT ENCODING DICT                      ,
    i_size                    TEXT ENCODING DICT                      ,
    i_formulation             TEXT ENCODING DICT                      ,
    i_color                   TEXT ENCODING DICT                      ,
    i_units                   TEXT ENCODING DICT                      ,
    i_container               TEXT ENCODING DICT                      ,
    i_manager_id              integer                       ,
    i_product_name            TEXT ENCODING DICT
);

create table store
(
    s_store_sk                integer               not null,
    s_store_id                TEXT NOT NULL ENCODING DICT            ,
    s_rec_start_date          date                          ,
    s_rec_end_date            date                          ,
    s_closed_date_sk          integer                       ,
    s_store_name              TEXT ENCODING DICT                   ,
    s_number_employees        integer                       ,
    s_floor_space             integer                       ,
    s_hours                   TEXT ENCODING DICT                      ,
    s_manager                 TEXT ENCODING DICT                   ,
    s_market_id               integer                       ,
    s_geography_class         TEXT ENCODING DICT                  ,
    s_market_desc             TEXT ENCODING DICT                  ,
    s_market_manager          TEXT ENCODING DICT                   ,
    s_division_id             integer                       ,
    s_division_name           TEXT ENCODING DICT                   ,
    s_company_id              integer                       ,
    s_company_name            TEXT ENCODING DICT                   ,
    s_street_number           TEXT ENCODING DICT                   ,
    s_street_name             TEXT ENCODING DICT                   ,
    s_street_type             TEXT ENCODING DICT                      ,
    s_suite_number            TEXT ENCODING DICT                      ,
    s_city                    TEXT ENCODING DICT                   ,
    s_county                  TEXT ENCODING DICT                   ,
    s_state                   TEXT ENCODING DICT                       ,
    s_zip                     TEXT ENCODING DICT                      ,
    s_country                 TEXT ENCODING DICT                   ,
    s_gmt_offset              decimal(5,2)                  ,
    s_tax_precentage          decimal(5,2)
);

create table call_center
(
    cc_call_center_sk         integer               not null,
    cc_call_center_id         TEXT NOT NULL ENCODING DICT            ,
    cc_rec_start_date         date                          ,
    cc_rec_end_date           date                          ,
    cc_closed_date_sk         integer                       ,
    cc_open_date_sk           integer                       ,
    cc_name                   TEXT ENCODING DICT                   ,
    cc_class                  TEXT ENCODING DICT                   ,
    cc_employees              integer                       ,
    cc_sq_ft                  integer                       ,
    cc_hours                  TEXT ENCODING DICT                      ,
    cc_manager                TEXT ENCODING DICT                   ,
    cc_mkt_id                 integer                       ,
    cc_mkt_class              TEXT ENCODING DICT                      ,
    cc_mkt_desc               TEXT ENCODING DICT                  ,
    cc_market_manager         TEXT ENCODING DICT                   ,
    cc_division               integer                       ,
    cc_division_name          TEXT ENCODING DICT                   ,
    cc_company                integer                       ,
    cc_company_name           TEXT ENCODING DICT                      ,
    cc_street_number          TEXT ENCODING DICT                      ,
    cc_street_name            TEXT ENCODING DICT                   ,
    cc_street_type            TEXT ENCODING DICT                      ,
    cc_suite_number           TEXT ENCODING DICT                      ,
    cc_city                   TEXT ENCODING DICT                   ,
    cc_county                 TEXT ENCODING DICT                   ,
    cc_state                  TEXT ENCODING DICT                       ,
    cc_zip                    TEXT ENCODING DICT                      ,
    cc_country                TEXT ENCODING DICT                   ,
    cc_gmt_offset             decimal(5,2)                  ,
    cc_tax_percentage         decimal(5,2)
);

create table customer
(
    c_customer_sk             integer               not null,
    c_customer_id             TEXT NOT NULL ENCODING DICT            ,
    c_current_cdemo_sk        integer                       ,
    c_current_hdemo_sk        integer                       ,
    c_current_addr_sk         integer                       ,
    c_first_shipto_date_sk    integer                       ,
    c_first_sales_date_sk     integer                       ,
    c_salutation              TEXT ENCODING DICT                      ,
    c_first_name              TEXT ENCODING DICT                      ,
    c_last_name               TEXT ENCODING DICT                      ,
    c_preferred_cust_flag     TEXT ENCODING DICT                       ,
    c_birth_day               integer                       ,
    c_birth_month             integer                       ,
    c_birth_year              integer                       ,
    c_birth_country           TEXT ENCODING DICT                   ,
    c_login                   TEXT ENCODING DICT                      ,
    c_email_address           TEXT ENCODING DICT                      ,
    c_last_review_date        TEXT ENCODING DICT
);

create table web_site
(
    web_site_sk               integer               not null,
    web_site_id               TEXT NOT NULL ENCODING DICT            ,
    web_rec_start_date        date                          ,
    web_rec_end_date          date                          ,
    web_name                  TEXT ENCODING DICT                   ,
    web_open_date_sk          integer                       ,
    web_close_date_sk         integer                       ,
    web_class                 TEXT ENCODING DICT                   ,
    web_manager               TEXT ENCODING DICT                   ,
    web_mkt_id                integer                       ,
    web_mkt_class             TEXT ENCODING DICT                   ,
    web_mkt_desc              TEXT ENCODING DICT                  ,
    web_market_manager        TEXT ENCODING DICT                   ,
    web_company_id            integer                       ,
    web_company_name          TEXT ENCODING DICT                      ,
    web_street_number         TEXT ENCODING DICT                      ,
    web_street_name           TEXT ENCODING DICT                   ,
    web_street_type           TEXT ENCODING DICT                      ,
    web_suite_number          TEXT ENCODING DICT                      ,
    web_city                  TEXT ENCODING DICT                   ,
    web_county                TEXT ENCODING DICT                   ,
    web_state                 TEXT ENCODING DICT                       ,
    web_zip                   TEXT ENCODING DICT                      ,
    web_country               TEXT ENCODING DICT                   ,
    web_gmt_offset            decimal(5,2)                  ,
    web_tax_percentage        decimal(5,2)
);

create table store_returns
(
    sr_returned_date_sk       integer                       ,
    sr_return_time_sk         integer                       ,
    sr_item_sk                integer               not null,
    sr_customer_sk            integer                       ,
    sr_cdemo_sk               integer                       ,
    sr_hdemo_sk               integer                       ,
    sr_addr_sk                integer                       ,
    sr_store_sk               integer                       ,
    sr_reason_sk              integer                       ,
    sr_ticket_number          integer               not null,
    sr_return_quantity        integer                       ,
    sr_return_amt             decimal(7,2)                  ,
    sr_return_tax             decimal(7,2)                  ,
    sr_return_amt_inc_tax     decimal(7,2)                  ,
    sr_fee                    decimal(7,2)                  ,
    sr_return_ship_cost       decimal(7,2)                  ,
    sr_refunded_cash          decimal(7,2)                  ,
    sr_reversed_charge        decimal(7,2)                  ,
    sr_store_credit           decimal(7,2)                  ,
    sr_net_loss               decimal(7,2)                  
);

create table household_demographics
(
    hd_demo_sk                integer               not null,
    hd_income_band_sk         integer                       ,
    hd_buy_potential          TEXT ENCODING DICT                      ,
    hd_dep_count              integer                       ,
    hd_vehicle_count          integer
);

create table web_page
(
    wp_web_page_sk            integer               not null,
    wp_web_page_id            TEXT NOT NULL ENCODING DICT            ,
    wp_rec_start_date         date                          ,
    wp_rec_end_date           date                          ,
    wp_creation_date_sk       integer                       ,
    wp_access_date_sk         integer                       ,
    wp_autogen_flag           TEXT ENCODING DICT                       ,
    wp_customer_sk            integer                       ,
    wp_url                    TEXT ENCODING DICT                  ,
    wp_type                   TEXT ENCODING DICT                      ,
    wp_char_count             integer                       ,
    wp_link_count             integer                       ,
    wp_image_count            integer                       ,
    wp_max_ad_count           integer
);

create table promotion
(
    p_promo_sk                integer               not null,
    p_promo_id                TEXT NOT NULL ENCODING DICT            ,
    p_start_date_sk           integer                       ,
    p_end_date_sk             integer                       ,
    p_item_sk                 integer                       ,
    p_cost                    decimal(15,2)                 ,
    p_response_target         integer                       ,
    p_promo_name              TEXT ENCODING DICT                      ,
    p_channel_dmail           TEXT ENCODING DICT                       ,
    p_channel_email           TEXT ENCODING DICT                       ,
    p_channel_catalog         TEXT ENCODING DICT                       ,
    p_channel_tv              TEXT ENCODING DICT                       ,
    p_channel_radio           TEXT ENCODING DICT                       ,
    p_channel_press           TEXT ENCODING DICT                       ,
    p_channel_event           TEXT ENCODING DICT                       ,
    p_channel_demo            TEXT ENCODING DICT                       ,
    p_channel_details         TEXT ENCODING DICT                  ,
    p_purpose                 TEXT ENCODING DICT                      ,
    p_discount_active         TEXT ENCODING DICT
);

create table catalog_page
(
    cp_catalog_page_sk        integer               not null,
    cp_catalog_page_id        TEXT NOT NULL ENCODING DICT            ,
    cp_start_date_sk          integer                       ,
    cp_end_date_sk            integer                       ,
    cp_department             TEXT ENCODING DICT                   ,
    cp_catalog_number         integer                       ,
    cp_catalog_page_number    integer                       ,
    cp_description            TEXT ENCODING DICT                  ,
    cp_type                   TEXT ENCODING DICT
);

create table inventory
(
    inv_date_sk               integer               not null,
    inv_item_sk               integer               not null,
    inv_warehouse_sk          integer               not null,
    inv_quantity_on_hand      integer
);

create table catalog_returns
(
    cr_returned_date_sk       integer                       ,
    cr_returned_time_sk       integer                       ,
    cr_item_sk                integer               not null,
    cr_refunded_customer_sk   integer                       ,
    cr_refunded_cdemo_sk      integer                       ,
    cr_refunded_hdemo_sk      integer                       ,
    cr_refunded_addr_sk       integer                       ,
    cr_returning_customer_sk  integer                       ,
    cr_returning_cdemo_sk     integer                       ,
    cr_returning_hdemo_sk     integer                       ,
    cr_returning_addr_sk      integer                       ,
    cr_call_center_sk         integer                       ,
    cr_catalog_page_sk        integer                       ,
    cr_ship_mode_sk           integer                       ,
    cr_warehouse_sk           integer                       ,
    cr_reason_sk              integer                       ,
    cr_order_number           integer               not null,
    cr_return_quantity        integer                       ,
    cr_return_amount          decimal(7,2)                  ,
    cr_return_tax             decimal(7,2)                  ,
    cr_return_amt_inc_tax     decimal(7,2)                  ,
    cr_fee                    decimal(7,2)                  ,
    cr_return_ship_cost       decimal(7,2)                  ,
    cr_refunded_cash          decimal(7,2)                  ,
    cr_reversed_charge        decimal(7,2)                  ,
    cr_store_credit           decimal(7,2)                  ,
    cr_net_loss               decimal(7,2)                  
);

create table web_returns
(
    wr_returned_date_sk       integer                       ,
    wr_returned_time_sk       integer                       ,
    wr_item_sk                integer               not null,
    wr_refunded_customer_sk   integer                       ,
    wr_refunded_cdemo_sk      integer                       ,
    wr_refunded_hdemo_sk      integer                       ,
    wr_refunded_addr_sk       integer                       ,
    wr_returning_customer_sk  integer                       ,
    wr_returning_cdemo_sk     integer                       ,
    wr_returning_hdemo_sk     integer                       ,
    wr_returning_addr_sk      integer                       ,
    wr_web_page_sk            integer                       ,
    wr_reason_sk              integer                       ,
    wr_order_number           integer               not null,
    wr_return_quantity        integer                       ,
    wr_return_amt             decimal(7,2)                  ,
    wr_return_tax             decimal(7,2)                  ,
    wr_return_amt_inc_tax     decimal(7,2)                  ,
    wr_fee                    decimal(7,2)                  ,
    wr_return_ship_cost       decimal(7,2)                  ,
    wr_refunded_cash          decimal(7,2)                  ,
    wr_reversed_charge        decimal(7,2)                  ,
    wr_account_credit         decimal(7,2)                  ,
    wr_net_loss               decimal(7,2)                  
);

create table web_sales
(
    ws_sold_date_sk           integer                       ,
    ws_sold_time_sk           integer                       ,
    ws_ship_date_sk           integer                       ,
    ws_item_sk                integer               not null,
    ws_bill_customer_sk       integer                       ,
    ws_bill_cdemo_sk          integer                       ,
    ws_bill_hdemo_sk          integer                       ,
    ws_bill_addr_sk           integer                       ,
    ws_ship_customer_sk       integer                       ,
    ws_ship_cdemo_sk          integer                       ,
    ws_ship_hdemo_sk          integer                       ,
    ws_ship_addr_sk           integer                       ,
    ws_web_page_sk            integer                       ,
    ws_web_site_sk            integer                       ,
    ws_ship_mode_sk           integer                       ,
    ws_warehouse_sk           integer                       ,
    ws_promo_sk               integer                       ,
    ws_order_number           integer               not null,
    ws_quantity               integer                       ,
    ws_wholesale_cost         decimal(7,2)                  ,
    ws_list_price             decimal(7,2)                  ,
    ws_sales_price            decimal(7,2)                  ,
    ws_ext_discount_amt       decimal(7,2)                  ,
    ws_ext_sales_price        decimal(7,2)                  ,
    ws_ext_wholesale_cost     decimal(7,2)                  ,
    ws_ext_list_price         decimal(7,2)                  ,
    ws_ext_tax                decimal(7,2)                  ,
    ws_coupon_amt             decimal(7,2)                  ,
    ws_ext_ship_cost          decimal(7,2)                  ,
    ws_net_paid               decimal(7,2)                  ,
    ws_net_paid_inc_tax       decimal(7,2)                  ,
    ws_net_paid_inc_ship      decimal(7,2)                  ,
    ws_net_paid_inc_ship_tax  decimal(7,2)                  ,
    ws_net_profit             decimal(7,2)                  
);

create table catalog_sales
(
    cs_sold_date_sk           integer                       ,
    cs_sold_time_sk           integer                       ,
    cs_ship_date_sk           integer                       ,
    cs_bill_customer_sk       integer                       ,
    cs_bill_cdemo_sk          integer                       ,
    cs_bill_hdemo_sk          integer                       ,
    cs_bill_addr_sk           integer                       ,
    cs_ship_customer_sk       integer                       ,
    cs_ship_cdemo_sk          integer                       ,
    cs_ship_hdemo_sk          integer                       ,
    cs_ship_addr_sk           integer                       ,
    cs_call_center_sk         integer                       ,
    cs_catalog_page_sk        integer                       ,
    cs_ship_mode_sk           integer                       ,
    cs_warehouse_sk           integer                       ,
    cs_item_sk                integer               not null,
    cs_promo_sk               integer                       ,
    cs_order_number           integer               not null,
    cs_quantity               integer                       ,
    cs_wholesale_cost         decimal(7,2)                  ,
    cs_list_price             decimal(7,2)                  ,
    cs_sales_price            decimal(7,2)                  ,
    cs_ext_discount_amt       decimal(7,2)                  ,
    cs_ext_sales_price        decimal(7,2)                  ,
    cs_ext_wholesale_cost     decimal(7,2)                  ,
    cs_ext_list_price         decimal(7,2)                  ,
    cs_ext_tax                decimal(7,2)                  ,
    cs_coupon_amt             decimal(7,2)                  ,
    cs_ext_ship_cost          decimal(7,2)                  ,
    cs_net_paid               decimal(7,2)                  ,
    cs_net_paid_inc_tax       decimal(7,2)                  ,
    cs_net_paid_inc_ship      decimal(7,2)                  ,
    cs_net_paid_inc_ship_tax  decimal(7,2)                  ,
    cs_net_profit             decimal(7,2)                  
);
create table store_sales
(
    ss_sold_date_sk           integer                       ,
    ss_sold_time_sk           integer                       ,
    ss_item_sk                integer               not null,
    ss_customer_sk            integer                       ,
    ss_cdemo_sk               integer                       ,
    ss_hdemo_sk               integer                       ,
    ss_addr_sk                integer                       ,
    ss_store_sk               integer                       ,
    ss_promo_sk               integer                       ,
    ss_ticket_number          integer               not null,
    ss_quantity               integer                       ,
    ss_wholesale_cost         decimal(7,2)                  ,
    ss_list_price             decimal(7,2)                  ,
    ss_sales_price            decimal(7,2)                  ,
    ss_ext_discount_amt       decimal(7,2)                  ,
    ss_ext_sales_price        decimal(7,2)                  ,
    ss_ext_wholesale_cost     decimal(7,2)                  ,
    ss_ext_list_price         decimal(7,2)                  ,
    ss_ext_tax                decimal(7,2)                  ,
    ss_coupon_amt             decimal(7,2)                  ,
    ss_net_paid               decimal(7,2)                  ,
    ss_net_paid_inc_tax       decimal(7,2)                  ,
    ss_net_profit             decimal(7,2)                  
);

