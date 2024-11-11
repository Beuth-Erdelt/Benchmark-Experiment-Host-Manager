#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"

######################## Show more parameters ########################
CHILD=$(cat /tmp/tpcds/CHILD )
echo "CHILD $CHILD"
echo "NUM_PODS $NUM_PODS"
echo "SF $SF"

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
    # store in (distributed) file system
    if test $NUM_PODS -gt 1
    then
        destination_raw=/data/tpcds/SF$SF/$NUM_PODS/$CHILD/
    else
        destination_raw=/data/tpcds/SF$SF/
    fi
else
    # only store locally
    destination_raw=/tmp/tpcds/
fi
echo "destination_raw $destination_raw"
cd $destination_raw

######################## Show generated files ########################
echo "Found these files:"
ls $destination_raw/*.dat -lh

######################## Wait until all pods of job are ready ########################
if test $BEXHOMA_SYNCH_LOAD -gt 0
then
    echo "Querying counter bexhoma-loader-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
    # add this pod to counter
    redis-cli -h 'bexhoma-messagequeue' incr "bexhoma-loader-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
    # wait for number of pods to be as expected
    while : ; do
        PODS_RUNNING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-loader-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
        echo "Found $PODS_RUNNING / $NUM_PODS running pods"
        if  test "$PODS_RUNNING" == $NUM_PODS
        then
            echo "OK"
            break
        elif test "$PODS_RUNNING" -gt $NUM_PODS
        then
            echo "Too many pods! Restart occured?"
            exit 0
        else
            echo "We have to wait"
            sleep 1
        fi
    done
fi

######################## Start measurement of time ########################
bexhoma_start_epoch=$(date -u +%s)
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"

######################## Execute loading ###################
# shuffled
#for i in `ls *.dat | shuf`; do
# ordered
for i in *.dat; do
    if test $NUM_PODS -gt 1
    then
        basename=${i%_"$CHILD"_"$NUM_PODS"*}
    else
        basename=${i%.dat*}
    fi
    wordcount=($(wc -l $i))
    lines=${wordcount[0]}
    # skip table if limit to other table is set
    if [ -z "${TPCDS_TABLE}" ]
    then
        echo "table limit not set"
    elif [ "${TPCDS_TABLE}" == "$basename" ]
    then
        echo "limit import to this table $TPCDS_TABLE"
    else
        echo "skipping $basename, import is limited to other table ($TPCDS_TABLE)"
        continue
    fi
    if [[ $basename == "call_center" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@cc_call_center_sk, @cc_call_center_id, @cc_rec_start_date, @cc_rec_end_date, @cc_closed_date_sk, @cc_open_date_sk, @cc_name, @cc_class, @cc_employees, @cc_sq_ft, @cc_hours, @cc_manager, @cc_mkt_id, @cc_mkt_class, @cc_mkt_desc, @cc_market_manager, @cc_division, @cc_division_name, @cc_company, @cc_company_name, @cc_street_number, @cc_street_name, @cc_street_type, @cc_suite_number, @cc_city, @cc_county, @cc_state, @cc_zip, @cc_country, @cc_gmt_offset, @cc_tax_percentage) SET cc_call_center_sk=NULLIF(@cc_call_center_sk,''), cc_call_center_id=NULLIF(@cc_call_center_id,''), cc_rec_start_date=NULLIF(@cc_rec_start_date,''), cc_rec_end_date=NULLIF(@cc_rec_end_date,''), cc_closed_date_sk=NULLIF(@cc_closed_date_sk,''), cc_open_date_sk=NULLIF(@cc_open_date_sk,''), cc_name=NULLIF(@cc_name,''), cc_class=NULLIF(@cc_class,''), cc_employees=NULLIF(@cc_employees,''), cc_sq_ft=NULLIF(@cc_sq_ft,''), cc_hours=NULLIF(@cc_hours,''), cc_manager=NULLIF(@cc_manager,''), cc_mkt_id=NULLIF(@cc_mkt_id,''), cc_mkt_class=NULLIF(@cc_mkt_class,''), cc_mkt_desc=NULLIF(@cc_mkt_desc,''), cc_market_manager=NULLIF(@cc_market_manager,''), cc_division=NULLIF(@cc_division,''), cc_division_name=NULLIF(@cc_division_name,''), cc_company=NULLIF(@cc_company,''), cc_company_name=NULLIF(@cc_company_name,''), cc_street_number=NULLIF(@cc_street_number,''), cc_street_name=NULLIF(@cc_street_name,''), cc_street_type=NULLIF(@cc_street_type,''), cc_suite_number=NULLIF(@cc_suite_number,''), cc_city=NULLIF(@cc_city,''), cc_county=NULLIF(@cc_county,''), cc_state=NULLIF(@cc_state,''), cc_zip=NULLIF(@cc_zip,''), cc_country=NULLIF(@cc_country,''), cc_gmt_offset=NULLIF(@cc_gmt_offset,''), cc_tax_percentage=NULLIF(@cc_tax_percentage,'')"
    fi
    if [[ $basename == "catalog_page" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@cp_catalog_page_sk, @cp_catalog_page_id, @cp_start_date_sk, @cp_end_date_sk, @cp_department, @cp_catalog_number, @cp_catalog_page_number, @cp_description, @cp_type) SET cp_catalog_page_sk=NULLIF(@cp_catalog_page_sk,''), cp_catalog_page_id=NULLIF(@cp_catalog_page_id,''), cp_start_date_sk=NULLIF(@cp_start_date_sk,''), cp_end_date_sk=NULLIF(@cp_end_date_sk,''), cp_department=NULLIF(@cp_department,''), cp_catalog_number=NULLIF(@cp_catalog_number,''), cp_catalog_page_number=NULLIF(@cp_catalog_page_number,''), cp_description=NULLIF(@cp_description,''), cp_type=NULLIF(@cp_type,'')"
    fi
    if [[ $basename == "catalog_returns" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@cr_returned_date_sk, @cr_returned_time_sk, @cr_item_sk, @cr_refunded_customer_sk, @cr_refunded_cdemo_sk, @cr_refunded_hdemo_sk, @cr_refunded_addr_sk, @cr_returning_customer_sk, @cr_returning_cdemo_sk, @cr_returning_hdemo_sk, @cr_returning_addr_sk, @cr_call_center_sk, @cr_catalog_page_sk, @cr_ship_mode_sk, @cr_warehouse_sk, @cr_reason_sk, @cr_order_number, @cr_return_quantity, @cr_return_amount, @cr_return_tax, @cr_return_amt_inc_tax, @cr_fee, @cr_return_ship_cost, @cr_refunded_cash, @cr_reversed_charge, @cr_store_credit, @cr_net_loss) SET cr_returned_date_sk=NULLIF(@cr_returned_date_sk,''), cr_returned_time_sk=NULLIF(@cr_returned_time_sk,''), cr_item_sk=NULLIF(@cr_item_sk,''), cr_refunded_customer_sk=NULLIF(@cr_refunded_customer_sk,''), cr_refunded_cdemo_sk=NULLIF(@cr_refunded_cdemo_sk,''), cr_refunded_hdemo_sk=NULLIF(@cr_refunded_hdemo_sk,''), cr_refunded_addr_sk=NULLIF(@cr_refunded_addr_sk,''), cr_returning_customer_sk=NULLIF(@cr_returning_customer_sk,''), cr_returning_cdemo_sk=NULLIF(@cr_returning_cdemo_sk,''), cr_returning_hdemo_sk=NULLIF(@cr_returning_hdemo_sk,''), cr_returning_addr_sk=NULLIF(@cr_returning_addr_sk,''), cr_call_center_sk=NULLIF(@cr_call_center_sk,''), cr_catalog_page_sk=NULLIF(@cr_catalog_page_sk,''), cr_ship_mode_sk=NULLIF(@cr_ship_mode_sk,''), cr_warehouse_sk=NULLIF(@cr_warehouse_sk,''), cr_reason_sk=NULLIF(@cr_reason_sk,''), cr_order_number=NULLIF(@cr_order_number,''), cr_return_quantity=NULLIF(@cr_return_quantity,''), cr_return_amount=NULLIF(@cr_return_amount,''), cr_return_tax=NULLIF(@cr_return_tax,''), cr_return_amt_inc_tax=NULLIF(@cr_return_amt_inc_tax,''), cr_fee=NULLIF(@cr_fee,''), cr_return_ship_cost=NULLIF(@cr_return_ship_cost,''), cr_refunded_cash=NULLIF(@cr_refunded_cash,''), cr_reversed_charge=NULLIF(@cr_reversed_charge,''), cr_store_credit=NULLIF(@cr_store_credit,''), cr_net_loss=NULLIF(@cr_net_loss,'')"
    fi
    if [[ $basename == "catalog_sales" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@cs_sold_date_sk, @cs_sold_time_sk, @cs_ship_date_sk, @cs_bill_customer_sk, @cs_bill_cdemo_sk, @cs_bill_hdemo_sk, @cs_bill_addr_sk, @cs_ship_customer_sk, @cs_ship_cdemo_sk, @cs_ship_hdemo_sk, @cs_ship_addr_sk, @cs_call_center_sk, @cs_catalog_page_sk, @cs_ship_mode_sk, @cs_warehouse_sk, @cs_item_sk, @cs_promo_sk, @cs_order_number, @cs_quantity, @cs_wholesale_cost, @cs_list_price, @cs_sales_price, @cs_ext_discount_amt, @cs_ext_sales_price, @cs_ext_wholesale_cost, @cs_ext_list_price, @cs_ext_tax, @cs_coupon_amt, @cs_ext_ship_cost, @cs_net_paid, @cs_net_paid_inc_tax, @cs_net_paid_inc_ship, @cs_net_paid_inc_ship_tax, @cs_net_profit) SET cs_sold_date_sk=NULLIF(@cs_sold_date_sk,''), cs_sold_time_sk=NULLIF(@cs_sold_time_sk,''), cs_ship_date_sk=NULLIF(@cs_ship_date_sk,''), cs_bill_customer_sk=NULLIF(@cs_bill_customer_sk,''), cs_bill_cdemo_sk=NULLIF(@cs_bill_cdemo_sk,''), cs_bill_hdemo_sk=NULLIF(@cs_bill_hdemo_sk,''), cs_bill_addr_sk=NULLIF(@cs_bill_addr_sk,''), cs_ship_customer_sk=NULLIF(@cs_ship_customer_sk,''), cs_ship_cdemo_sk=NULLIF(@cs_ship_cdemo_sk,''), cs_ship_hdemo_sk=NULLIF(@cs_ship_hdemo_sk,''), cs_ship_addr_sk=NULLIF(@cs_ship_addr_sk,''), cs_call_center_sk=NULLIF(@cs_call_center_sk,''), cs_catalog_page_sk=NULLIF(@cs_catalog_page_sk,''), cs_ship_mode_sk=NULLIF(@cs_ship_mode_sk,''), cs_warehouse_sk=NULLIF(@cs_warehouse_sk,''), cs_item_sk=NULLIF(@cs_item_sk,''), cs_promo_sk=NULLIF(@cs_promo_sk,''), cs_order_number=NULLIF(@cs_order_number,''), cs_quantity=NULLIF(@cs_quantity,''), cs_wholesale_cost=NULLIF(@cs_wholesale_cost,''), cs_list_price=NULLIF(@cs_list_price,''), cs_sales_price=NULLIF(@cs_sales_price,''), cs_ext_discount_amt=NULLIF(@cs_ext_discount_amt,''), cs_ext_sales_price=NULLIF(@cs_ext_sales_price,''), cs_ext_wholesale_cost=NULLIF(@cs_ext_wholesale_cost,''), cs_ext_list_price=NULLIF(@cs_ext_list_price,''), cs_ext_tax=NULLIF(@cs_ext_tax,''), cs_coupon_amt=NULLIF(@cs_coupon_amt,''), cs_ext_ship_cost=NULLIF(@cs_ext_ship_cost,''), cs_net_paid=NULLIF(@cs_net_paid,''), cs_net_paid_inc_tax=NULLIF(@cs_net_paid_inc_tax,''), cs_net_paid_inc_ship=NULLIF(@cs_net_paid_inc_ship,''), cs_net_paid_inc_ship_tax=NULLIF(@cs_net_paid_inc_ship_tax,''), cs_net_profit=NULLIF(@cs_net_profit,'')"
    fi
    if [[ $basename == "customer" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@c_customer_sk, @c_customer_id, @c_current_cdemo_sk, @c_current_hdemo_sk, @c_current_addr_sk, @c_first_shipto_date_sk, @c_first_sales_date_sk, @c_salutation, @c_first_name, @c_last_name, @c_preferred_cust_flag, @c_birth_day, @c_birth_month, @c_birth_year, @c_birth_country, @c_login, @c_email_address, @c_last_review_date) SET c_customer_sk=NULLIF(@c_customer_sk,''), c_customer_id=NULLIF(@c_customer_id,''), c_current_cdemo_sk=NULLIF(@c_current_cdemo_sk,''), c_current_hdemo_sk=NULLIF(@c_current_hdemo_sk,''), c_current_addr_sk=NULLIF(@c_current_addr_sk,''), c_first_shipto_date_sk=NULLIF(@c_first_shipto_date_sk,''), c_first_sales_date_sk=NULLIF(@c_first_sales_date_sk,''), c_salutation=NULLIF(@c_salutation,''), c_first_name=NULLIF(@c_first_name,''), c_last_name=NULLIF(@c_last_name,''), c_preferred_cust_flag=NULLIF(@c_preferred_cust_flag,''), c_birth_day=NULLIF(@c_birth_day,''), c_birth_month=NULLIF(@c_birth_month,''), c_birth_year=NULLIF(@c_birth_year,''), c_birth_country=NULLIF(@c_birth_country,''), c_login=NULLIF(@c_login,''), c_email_address=NULLIF(@c_email_address,''), c_last_review_date=NULLIF(@c_last_review_date,'')"
    fi
    if [[ $basename == "customer_address" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@ca_address_sk, @ca_address_id, @ca_street_number, @ca_street_name, @ca_street_type, @ca_suite_number, @ca_city, @ca_county, @ca_state, @ca_zip, @ca_country, @ca_gmt_offset, @ca_location_type) SET ca_address_sk=NULLIF(@ca_address_sk,''), ca_address_id=NULLIF(@ca_address_id,''), ca_street_number=NULLIF(@ca_street_number,''), ca_street_name=NULLIF(@ca_street_name,''), ca_street_type=NULLIF(@ca_street_type,''), ca_suite_number=NULLIF(@ca_suite_number,''), ca_city=NULLIF(@ca_city,''), ca_county=NULLIF(@ca_county,''), ca_state=NULLIF(@ca_state,''), ca_zip=NULLIF(@ca_zip,''), ca_country=NULLIF(@ca_country,''), ca_gmt_offset=NULLIF(@ca_gmt_offset,''), ca_location_type=NULLIF(@ca_location_type,'')"
    fi
    if [[ $basename == "customer_demographics" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@cd_demo_sk, @cd_gender, @cd_marital_status, @cd_education_status, @cd_purchase_estimate, @cd_credit_rating, @cd_dep_count, @cd_dep_employed_count, @cd_dep_college_count) SET cd_demo_sk=NULLIF(@cd_demo_sk,''), cd_gender=NULLIF(@cd_gender,''), cd_marital_status=NULLIF(@cd_marital_status,''), cd_education_status=NULLIF(@cd_education_status,''), cd_purchase_estimate=NULLIF(@cd_purchase_estimate,''), cd_credit_rating=NULLIF(@cd_credit_rating,''), cd_dep_count=NULLIF(@cd_dep_count,''), cd_dep_employed_count=NULLIF(@cd_dep_employed_count,''), cd_dep_college_count=NULLIF(@cd_dep_college_count,'')"
    fi
    if [[ $basename == "date_dim" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@d_date_sk, @d_date_id, @d_date, @d_month_seq, @d_week_seq, @d_quarter_seq, @d_year, @d_dow, @d_moy, @d_dom, @d_qoy, @d_fy_year, @d_fy_quarter_seq, @d_fy_week_seq, @d_day_name, @d_quarter_name, @d_holiday, @d_weekend, @d_following_holiday, @d_first_dom, @d_last_dom, @d_same_day_ly, @d_same_day_lq, @d_current_day, @d_current_week, @d_current_month, @d_current_quarter, @d_current_year) SET d_date_sk=NULLIF(@d_date_sk,''), d_date_id=NULLIF(@d_date_id,''), d_date=NULLIF(@d_date,''), d_month_seq=NULLIF(@d_month_seq,''), d_week_seq=NULLIF(@d_week_seq,''), d_quarter_seq=NULLIF(@d_quarter_seq,''), d_year=NULLIF(@d_year,''), d_dow=NULLIF(@d_dow,''), d_moy=NULLIF(@d_moy,''), d_dom=NULLIF(@d_dom,''), d_qoy=NULLIF(@d_qoy,''), d_fy_year=NULLIF(@d_fy_year,''), d_fy_quarter_seq=NULLIF(@d_fy_quarter_seq,''), d_fy_week_seq=NULLIF(@d_fy_week_seq,''), d_day_name=NULLIF(@d_day_name,''), d_quarter_name=NULLIF(@d_quarter_name,''), d_holiday=NULLIF(@d_holiday,''), d_weekend=NULLIF(@d_weekend,''), d_following_holiday=NULLIF(@d_following_holiday,''), d_first_dom=NULLIF(@d_first_dom,''), d_last_dom=NULLIF(@d_last_dom,''), d_same_day_ly=NULLIF(@d_same_day_ly,''), d_same_day_lq=NULLIF(@d_same_day_lq,''), d_current_day=NULLIF(@d_current_day,''), d_current_week=NULLIF(@d_current_week,''), d_current_month=NULLIF(@d_current_month,''), d_current_quarter=NULLIF(@d_current_quarter,''), d_current_year=NULLIF(@d_current_year,'')"
    fi
    if [[ $basename == "dbgen_version" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@dv_version, @dv_create_date, @dv_create_time, @dv_cmdline_args) SET dv_version=NULLIF(@dv_version,''), dv_create_date=NULLIF(@dv_create_date,''), dv_create_time=NULLIF(@dv_create_time,''), dv_cmdline_args=NULLIF(@dv_cmdline_args,'')"
    fi
    if [[ $basename == "household_demographics" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@hd_demo_sk, @hd_income_band_sk, @hd_buy_potential, @hd_dep_count, @hd_vehicle_count) SET hd_demo_sk=NULLIF(@hd_demo_sk,''), hd_income_band_sk=NULLIF(@hd_income_band_sk,''), hd_buy_potential=NULLIF(@hd_buy_potential,''), hd_dep_count=NULLIF(@hd_dep_count,''), hd_vehicle_count=NULLIF(@hd_vehicle_count,'')"
    fi
    if [[ $basename == "income_band" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@ib_income_band_sk, @ib_lower_bound, @ib_upper_bound) SET ib_income_band_sk=NULLIF(@ib_income_band_sk,''), ib_lower_bound=NULLIF(@ib_lower_bound,''), ib_upper_bound=NULLIF(@ib_upper_bound,'')"
    fi
    if [[ $basename == "inventory" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@inv_date_sk, @inv_item_sk, @inv_warehouse_sk, @inv_quantity_on_hand) SET inv_date_sk=NULLIF(@inv_date_sk,''), inv_item_sk=NULLIF(@inv_item_sk,''), inv_warehouse_sk=NULLIF(@inv_warehouse_sk,''), inv_quantity_on_hand=NULLIF(@inv_quantity_on_hand,'')"
    fi
    if [[ $basename == "item" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@i_item_sk, @i_item_id, @i_rec_start_date, @i_rec_end_date, @i_item_desc, @i_current_price, @i_wholesale_cost, @i_brand_id, @i_brand, @i_class_id, @i_class, @i_category_id, @i_category, @i_manufact_id, @i_manufact, @i_size, @i_formulation, @i_color, @i_units, @i_container, @i_manager_id, @i_product_name) SET i_item_sk=NULLIF(@i_item_sk,''), i_item_id=NULLIF(@i_item_id,''), i_rec_start_date=NULLIF(@i_rec_start_date,''), i_rec_end_date=NULLIF(@i_rec_end_date,''), i_item_desc=NULLIF(@i_item_desc,''), i_current_price=NULLIF(@i_current_price,''), i_wholesale_cost=NULLIF(@i_wholesale_cost,''), i_brand_id=NULLIF(@i_brand_id,''), i_brand=NULLIF(@i_brand,''), i_class_id=NULLIF(@i_class_id,''), i_class=NULLIF(@i_class,''), i_category_id=NULLIF(@i_category_id,''), i_category=NULLIF(@i_category,''), i_manufact_id=NULLIF(@i_manufact_id,''), i_manufact=NULLIF(@i_manufact,''), i_size=NULLIF(@i_size,''), i_formulation=NULLIF(@i_formulation,''), i_color=NULLIF(@i_color,''), i_units=NULLIF(@i_units,''), i_container=NULLIF(@i_container,''), i_manager_id=NULLIF(@i_manager_id,''), i_product_name=NULLIF(@i_product_name,'')"
    fi
    if [[ $basename == "promotion" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@p_promo_sk, @p_promo_id, @p_start_date_sk, @p_end_date_sk, @p_item_sk, @p_cost, @p_response_target, @p_promo_name, @p_channel_dmail, @p_channel_email, @p_channel_catalog, @p_channel_tv, @p_channel_radio, @p_channel_press, @p_channel_event, @p_channel_demo, @p_channel_details, @p_purpose, @p_discount_active) SET p_promo_sk=NULLIF(@p_promo_sk,''), p_promo_id=NULLIF(@p_promo_id,''), p_start_date_sk=NULLIF(@p_start_date_sk,''), p_end_date_sk=NULLIF(@p_end_date_sk,''), p_item_sk=NULLIF(@p_item_sk,''), p_cost=NULLIF(@p_cost,''), p_response_target=NULLIF(@p_response_target,''), p_promo_name=NULLIF(@p_promo_name,''), p_channel_dmail=NULLIF(@p_channel_dmail,''), p_channel_email=NULLIF(@p_channel_email,''), p_channel_catalog=NULLIF(@p_channel_catalog,''), p_channel_tv=NULLIF(@p_channel_tv,''), p_channel_radio=NULLIF(@p_channel_radio,''), p_channel_press=NULLIF(@p_channel_press,''), p_channel_event=NULLIF(@p_channel_event,''), p_channel_demo=NULLIF(@p_channel_demo,''), p_channel_details=NULLIF(@p_channel_details,''), p_purpose=NULLIF(@p_purpose,''), p_discount_active=NULLIF(@p_discount_active,'')"
    fi
    if [[ $basename == "reason" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@r_reason_sk, @r_reason_id, @r_reason_desc) SET r_reason_sk=NULLIF(@r_reason_sk,''), r_reason_id=NULLIF(@r_reason_id,''), r_reason_desc=NULLIF(@r_reason_desc,'')"
    fi
    if [[ $basename == "ship_mode" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@sm_ship_mode_sk, @sm_ship_mode_id, @sm_type, @sm_code, @sm_carrier, @sm_contract) SET sm_ship_mode_sk=NULLIF(@sm_ship_mode_sk,''), sm_ship_mode_id=NULLIF(@sm_ship_mode_id,''), sm_type=NULLIF(@sm_type,''), sm_code=NULLIF(@sm_code,''), sm_carrier=NULLIF(@sm_carrier,''), sm_contract=NULLIF(@sm_contract,'')"
    fi
    if [[ $basename == "store" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@s_store_sk, @s_store_id, @s_rec_start_date, @s_rec_end_date, @s_closed_date_sk, @s_store_name, @s_number_employees, @s_floor_space, @s_hours, @s_manager, @s_market_id, @s_geography_class, @s_market_desc, @s_market_manager, @s_division_id, @s_division_name, @s_company_id, @s_company_name, @s_street_number, @s_street_name, @s_street_type, @s_suite_number, @s_city, @s_county, @s_state, @s_zip, @s_country, @s_gmt_offset, @s_tax_precentage) SET s_store_sk=NULLIF(@s_store_sk,''), s_store_id=NULLIF(@s_store_id,''), s_rec_start_date=NULLIF(@s_rec_start_date,''), s_rec_end_date=NULLIF(@s_rec_end_date,''), s_closed_date_sk=NULLIF(@s_closed_date_sk,''), s_store_name=NULLIF(@s_store_name,''), s_number_employees=NULLIF(@s_number_employees,''), s_floor_space=NULLIF(@s_floor_space,''), s_hours=NULLIF(@s_hours,''), s_manager=NULLIF(@s_manager,''), s_market_id=NULLIF(@s_market_id,''), s_geography_class=NULLIF(@s_geography_class,''), s_market_desc=NULLIF(@s_market_desc,''), s_market_manager=NULLIF(@s_market_manager,''), s_division_id=NULLIF(@s_division_id,''), s_division_name=NULLIF(@s_division_name,''), s_company_id=NULLIF(@s_company_id,''), s_company_name=NULLIF(@s_company_name,''), s_street_number=NULLIF(@s_street_number,''), s_street_name=NULLIF(@s_street_name,''), s_street_type=NULLIF(@s_street_type,''), s_suite_number=NULLIF(@s_suite_number,''), s_city=NULLIF(@s_city,''), s_county=NULLIF(@s_county,''), s_state=NULLIF(@s_state,''), s_zip=NULLIF(@s_zip,''), s_country=NULLIF(@s_country,''), s_gmt_offset=NULLIF(@s_gmt_offset,''), s_tax_precentage=NULLIF(@s_tax_precentage,'')"
    fi
    if [[ $basename == "store_returns" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@sr_returned_date_sk, @sr_return_time_sk, @sr_item_sk, @sr_customer_sk, @sr_cdemo_sk, @sr_hdemo_sk, @sr_addr_sk, @sr_store_sk, @sr_reason_sk, @sr_ticket_number, @sr_return_quantity, @sr_return_amt, @sr_return_tax, @sr_return_amt_inc_tax, @sr_fee, @sr_return_ship_cost, @sr_refunded_cash, @sr_reversed_charge, @sr_store_credit, @sr_net_loss) SET sr_returned_date_sk=NULLIF(@sr_returned_date_sk,''), sr_return_time_sk=NULLIF(@sr_return_time_sk,''), sr_item_sk=NULLIF(@sr_item_sk,''), sr_customer_sk=NULLIF(@sr_customer_sk,''), sr_cdemo_sk=NULLIF(@sr_cdemo_sk,''), sr_hdemo_sk=NULLIF(@sr_hdemo_sk,''), sr_addr_sk=NULLIF(@sr_addr_sk,''), sr_store_sk=NULLIF(@sr_store_sk,''), sr_reason_sk=NULLIF(@sr_reason_sk,''), sr_ticket_number=NULLIF(@sr_ticket_number,''), sr_return_quantity=NULLIF(@sr_return_quantity,''), sr_return_amt=NULLIF(@sr_return_amt,''), sr_return_tax=NULLIF(@sr_return_tax,''), sr_return_amt_inc_tax=NULLIF(@sr_return_amt_inc_tax,''), sr_fee=NULLIF(@sr_fee,''), sr_return_ship_cost=NULLIF(@sr_return_ship_cost,''), sr_refunded_cash=NULLIF(@sr_refunded_cash,''), sr_reversed_charge=NULLIF(@sr_reversed_charge,''), sr_store_credit=NULLIF(@sr_store_credit,''), sr_net_loss=NULLIF(@sr_net_loss,'')"
    fi
    if [[ $basename == "store_sales" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@ss_sold_date_sk, @ss_sold_time_sk, @ss_item_sk, @ss_customer_sk, @ss_cdemo_sk, @ss_hdemo_sk, @ss_addr_sk, @ss_store_sk, @ss_promo_sk, @ss_ticket_number, @ss_quantity, @ss_wholesale_cost, @ss_list_price, @ss_sales_price, @ss_ext_discount_amt, @ss_ext_sales_price, @ss_ext_wholesale_cost, @ss_ext_list_price, @ss_ext_tax, @ss_coupon_amt, @ss_net_paid, @ss_net_paid_inc_tax, @ss_net_profit) SET ss_sold_date_sk=NULLIF(@ss_sold_date_sk,''), ss_sold_time_sk=NULLIF(@ss_sold_time_sk,''), ss_item_sk=NULLIF(@ss_item_sk,''), ss_customer_sk=NULLIF(@ss_customer_sk,''), ss_cdemo_sk=NULLIF(@ss_cdemo_sk,''), ss_hdemo_sk=NULLIF(@ss_hdemo_sk,''), ss_addr_sk=NULLIF(@ss_addr_sk,''), ss_store_sk=NULLIF(@ss_store_sk,''), ss_promo_sk=NULLIF(@ss_promo_sk,''), ss_ticket_number=NULLIF(@ss_ticket_number,''), ss_quantity=NULLIF(@ss_quantity,''), ss_wholesale_cost=NULLIF(@ss_wholesale_cost,''), ss_list_price=NULLIF(@ss_list_price,''), ss_sales_price=NULLIF(@ss_sales_price,''), ss_ext_discount_amt=NULLIF(@ss_ext_discount_amt,''), ss_ext_sales_price=NULLIF(@ss_ext_sales_price,''), ss_ext_wholesale_cost=NULLIF(@ss_ext_wholesale_cost,''), ss_ext_list_price=NULLIF(@ss_ext_list_price,''), ss_ext_tax=NULLIF(@ss_ext_tax,''), ss_coupon_amt=NULLIF(@ss_coupon_amt,''), ss_net_paid=NULLIF(@ss_net_paid,''), ss_net_paid_inc_tax=NULLIF(@ss_net_paid_inc_tax,''), ss_net_profit=NULLIF(@ss_net_profit,'')"
    fi
    if [[ $basename == "time_dim" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@t_time_sk, @t_time_id, @t_time, @t_hour, @t_minute, @t_second, @t_am_pm, @t_shift, @t_sub_shift, @t_meal_time) SET t_time_sk=NULLIF(@t_time_sk,''), t_time_id=NULLIF(@t_time_id,''), t_time=NULLIF(@t_time,''), t_hour=NULLIF(@t_hour,''), t_minute=NULLIF(@t_minute,''), t_second=NULLIF(@t_second,''), t_am_pm=NULLIF(@t_am_pm,''), t_shift=NULLIF(@t_shift,''), t_sub_shift=NULLIF(@t_sub_shift,''), t_meal_time=NULLIF(@t_meal_time,'')"
    fi
    if [[ $basename == "warehouse" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@w_warehouse_sk, @w_warehouse_id, @w_warehouse_name, @w_warehouse_sq_ft, @w_street_number, @w_street_name, @w_street_type, @w_suite_number, @w_city, @w_county, @w_state, @w_zip, @w_country, @w_gmt_offset) SET w_warehouse_sk=NULLIF(@w_warehouse_sk,''), w_warehouse_id=NULLIF(@w_warehouse_id,''), w_warehouse_name=NULLIF(@w_warehouse_name,''), w_warehouse_sq_ft=NULLIF(@w_warehouse_sq_ft,''), w_street_number=NULLIF(@w_street_number,''), w_street_name=NULLIF(@w_street_name,''), w_street_type=NULLIF(@w_street_type,''), w_suite_number=NULLIF(@w_suite_number,''), w_city=NULLIF(@w_city,''), w_county=NULLIF(@w_county,''), w_state=NULLIF(@w_state,''), w_zip=NULLIF(@w_zip,''), w_country=NULLIF(@w_country,''), w_gmt_offset=NULLIF(@w_gmt_offset,'')"
    fi
    if [[ $basename == "web_page" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@wp_web_page_sk, @wp_web_page_id, @wp_rec_start_date, @wp_rec_end_date, @wp_creation_date_sk, @wp_access_date_sk, @wp_autogen_flag, @wp_customer_sk, @wp_url, @wp_type, @wp_char_count, @wp_link_count, @wp_image_count, @wp_max_ad_count) SET wp_web_page_sk=NULLIF(@wp_web_page_sk,''), wp_web_page_id=NULLIF(@wp_web_page_id,''), wp_rec_start_date=NULLIF(@wp_rec_start_date,''), wp_rec_end_date=NULLIF(@wp_rec_end_date,''), wp_creation_date_sk=NULLIF(@wp_creation_date_sk,''), wp_access_date_sk=NULLIF(@wp_access_date_sk,''), wp_autogen_flag=NULLIF(@wp_autogen_flag,''), wp_customer_sk=NULLIF(@wp_customer_sk,''), wp_url=NULLIF(@wp_url,''), wp_type=NULLIF(@wp_type,''), wp_char_count=NULLIF(@wp_char_count,''), wp_link_count=NULLIF(@wp_link_count,''), wp_image_count=NULLIF(@wp_image_count,''), wp_max_ad_count=NULLIF(@wp_max_ad_count,'')"
    fi
    if [[ $basename == "web_returns" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@wr_returned_date_sk, @wr_returned_time_sk, @wr_item_sk, @wr_refunded_customer_sk, @wr_refunded_cdemo_sk, @wr_refunded_hdemo_sk, @wr_refunded_addr_sk, @wr_returning_customer_sk, @wr_returning_cdemo_sk, @wr_returning_hdemo_sk, @wr_returning_addr_sk, @wr_web_page_sk, @wr_reason_sk, @wr_order_number, @wr_return_quantity, @wr_return_amt, @wr_return_tax, @wr_return_amt_inc_tax, @wr_fee, @wr_return_ship_cost, @wr_refunded_cash, @wr_reversed_charge, @wr_account_credit, @wr_net_loss) SET wr_returned_date_sk=NULLIF(@wr_returned_date_sk,''), wr_returned_time_sk=NULLIF(@wr_returned_time_sk,''), wr_item_sk=NULLIF(@wr_item_sk,''), wr_refunded_customer_sk=NULLIF(@wr_refunded_customer_sk,''), wr_refunded_cdemo_sk=NULLIF(@wr_refunded_cdemo_sk,''), wr_refunded_hdemo_sk=NULLIF(@wr_refunded_hdemo_sk,''), wr_refunded_addr_sk=NULLIF(@wr_refunded_addr_sk,''), wr_returning_customer_sk=NULLIF(@wr_returning_customer_sk,''), wr_returning_cdemo_sk=NULLIF(@wr_returning_cdemo_sk,''), wr_returning_hdemo_sk=NULLIF(@wr_returning_hdemo_sk,''), wr_returning_addr_sk=NULLIF(@wr_returning_addr_sk,''), wr_web_page_sk=NULLIF(@wr_web_page_sk,''), wr_reason_sk=NULLIF(@wr_reason_sk,''), wr_order_number=NULLIF(@wr_order_number,''), wr_return_quantity=NULLIF(@wr_return_quantity,''), wr_return_amt=NULLIF(@wr_return_amt,''), wr_return_tax=NULLIF(@wr_return_tax,''), wr_return_amt_inc_tax=NULLIF(@wr_return_amt_inc_tax,''), wr_fee=NULLIF(@wr_fee,''), wr_return_ship_cost=NULLIF(@wr_return_ship_cost,''), wr_refunded_cash=NULLIF(@wr_refunded_cash,''), wr_reversed_charge=NULLIF(@wr_reversed_charge,''), wr_account_credit=NULLIF(@wr_account_credit,''), wr_net_loss=NULLIF(@wr_net_loss,'')"
    fi
    if [[ $basename == "web_sales" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@ws_sold_date_sk, @ws_sold_time_sk, @ws_ship_date_sk, @ws_item_sk, @ws_bill_customer_sk, @ws_bill_cdemo_sk, @ws_bill_hdemo_sk, @ws_bill_addr_sk, @ws_ship_customer_sk, @ws_ship_cdemo_sk, @ws_ship_hdemo_sk, @ws_ship_addr_sk, @ws_web_page_sk, @ws_web_site_sk, @ws_ship_mode_sk, @ws_warehouse_sk, @ws_promo_sk, @ws_order_number, @ws_quantity, @ws_wholesale_cost, @ws_list_price, @ws_sales_price, @ws_ext_discount_amt, @ws_ext_sales_price, @ws_ext_wholesale_cost, @ws_ext_list_price, @ws_ext_tax, @ws_coupon_amt, @ws_ext_ship_cost, @ws_net_paid, @ws_net_paid_inc_tax, @ws_net_paid_inc_ship, @ws_net_paid_inc_ship_tax, @ws_net_profit) SET ws_sold_date_sk=NULLIF(@ws_sold_date_sk,''), ws_sold_time_sk=NULLIF(@ws_sold_time_sk,''), ws_ship_date_sk=NULLIF(@ws_ship_date_sk,''), ws_item_sk=NULLIF(@ws_item_sk,''), ws_bill_customer_sk=NULLIF(@ws_bill_customer_sk,''), ws_bill_cdemo_sk=NULLIF(@ws_bill_cdemo_sk,''), ws_bill_hdemo_sk=NULLIF(@ws_bill_hdemo_sk,''), ws_bill_addr_sk=NULLIF(@ws_bill_addr_sk,''), ws_ship_customer_sk=NULLIF(@ws_ship_customer_sk,''), ws_ship_cdemo_sk=NULLIF(@ws_ship_cdemo_sk,''), ws_ship_hdemo_sk=NULLIF(@ws_ship_hdemo_sk,''), ws_ship_addr_sk=NULLIF(@ws_ship_addr_sk,''), ws_web_page_sk=NULLIF(@ws_web_page_sk,''), ws_web_site_sk=NULLIF(@ws_web_site_sk,''), ws_ship_mode_sk=NULLIF(@ws_ship_mode_sk,''), ws_warehouse_sk=NULLIF(@ws_warehouse_sk,''), ws_promo_sk=NULLIF(@ws_promo_sk,''), ws_order_number=NULLIF(@ws_order_number,''), ws_quantity=NULLIF(@ws_quantity,''), ws_wholesale_cost=NULLIF(@ws_wholesale_cost,''), ws_list_price=NULLIF(@ws_list_price,''), ws_sales_price=NULLIF(@ws_sales_price,''), ws_ext_discount_amt=NULLIF(@ws_ext_discount_amt,''), ws_ext_sales_price=NULLIF(@ws_ext_sales_price,''), ws_ext_wholesale_cost=NULLIF(@ws_ext_wholesale_cost,''), ws_ext_list_price=NULLIF(@ws_ext_list_price,''), ws_ext_tax=NULLIF(@ws_ext_tax,''), ws_coupon_amt=NULLIF(@ws_coupon_amt,''), ws_ext_ship_cost=NULLIF(@ws_ext_ship_cost,''), ws_net_paid=NULLIF(@ws_net_paid,''), ws_net_paid_inc_tax=NULLIF(@ws_net_paid_inc_tax,''), ws_net_paid_inc_ship=NULLIF(@ws_net_paid_inc_ship,''), ws_net_paid_inc_ship_tax=NULLIF(@ws_net_paid_inc_ship_tax,''), ws_net_profit=NULLIF(@ws_net_profit,'')"
    fi
    if [[ $basename == "web_site" ]]
    then
        COMMAND="LOAD DATA LOCAL INFILE '$i' INTO TABLE $basename FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '\"'
(@web_site_sk, @web_site_id, @web_rec_start_date, @web_rec_end_date, @web_name, @web_open_date_sk, @web_close_date_sk, @web_class, @web_manager, @web_mkt_id, @web_mkt_class, @web_mkt_desc, @web_market_manager, @web_company_id, @web_company_name, @web_street_number, @web_street_name, @web_street_type, @web_suite_number, @web_city, @web_county, @web_state, @web_zip, @web_country, @web_gmt_offset, @web_tax_percentage) SET web_site_sk=NULLIF(@web_site_sk,''), web_site_id=NULLIF(@web_site_id,''), web_rec_start_date=NULLIF(@web_rec_start_date,''), web_rec_end_date=NULLIF(@web_rec_end_date,''), web_name=NULLIF(@web_name,''), web_open_date_sk=NULLIF(@web_open_date_sk,''), web_close_date_sk=NULLIF(@web_close_date_sk,''), web_class=NULLIF(@web_class,''), web_manager=NULLIF(@web_manager,''), web_mkt_id=NULLIF(@web_mkt_id,''), web_mkt_class=NULLIF(@web_mkt_class,''), web_mkt_desc=NULLIF(@web_mkt_desc,''), web_market_manager=NULLIF(@web_market_manager,''), web_company_id=NULLIF(@web_company_id,''), web_company_name=NULLIF(@web_company_name,''), web_street_number=NULLIF(@web_street_number,''), web_street_name=NULLIF(@web_street_name,''), web_street_type=NULLIF(@web_street_type,''), web_suite_number=NULLIF(@web_suite_number,''), web_city=NULLIF(@web_city,''), web_county=NULLIF(@web_county,''), web_state=NULLIF(@web_state,''), web_zip=NULLIF(@web_zip,''), web_country=NULLIF(@web_country,''), web_gmt_offset=NULLIF(@web_gmt_offset,''), web_tax_percentage=NULLIF(@web_tax_percentage,'')"
    fi
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|','\\n','\"' NULL AS ''"
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|' NULL AS ''"
    echo "============================"
    echo "$COMMAND"
    #OUTPUT="$(mclient --host $BEXHOMA_HOST --database $DATABASE --port $BEXHOMA_PORT -s \"COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|' NULL AS ''\" - < $i)"

    #FAILED=0 # everything ok
    #FAILED=1 # known error
    #FAILED=2 # unknown error
    FAILED=1
    while [ $FAILED == 1 ]
    do
        FAILED=2
        SECONDS_START=$SECONDS
        echo "=========="
        time mysqlsh --host $BEXHOMA_HOST --database $DATABASE --port $BEXHOMA_PORT -e "$COMMAND" &> /tmp/OUTPUT.txt
        echo "Start $SECONDS_START seconds"
        SECONDS_END=$SECONDS
        echo "End $SECONDS_END seconds"
        DURATION=$((SECONDS_END-SECONDS_START))
        echo "Duration $DURATION seconds"
        #mclient --host $BEXHOMA_HOST --database $DATABASE --port $BEXHOMA_PORT -E UTF-8 -L import.log -s "$COMMAND" - < $i &>OUTPUT.txt
        #mclient --host $BEXHOMA_HOST --database $DATABASE --port $BEXHOMA_PORT -s "COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|','\\n','\"' NULL AS ''" - < $i &>OUTPUT.txt
        #cat import.log
        OUTPUT=$(cat /tmp/OUTPUT.txt )
        echo "$OUTPUT"
        FAILED=0
        # everything worked well ("row" and "rows" string checked)
        if [[ $OUTPUT == *"$lines affected row"* ]]; then echo "Import ok"; FAILED=0; fi
        # rollback, we have to do it again (?)
        if [[ $OUTPUT == *"ROLLBACK"* ]]; then echo "ROLLBACK occured"; FAILED=1; fi
        # no thread left, we have to do it again (?)
        #if [[ $OUTPUT == *"failed to start worker thread"* ]]; then echo "No worker thread"; FAILED=1; fi
        #if [[ $OUTPUT == *"failed to start producer thread"* ]]; then echo "No producer thread"; FAILED=1; fi
        #if [[ $OUTPUT == *"Challenge string is not valid, it is empty"* ]]; then echo "No Login possible"; FAILED=1; fi
        # something else - what?
        if [[ $OUTPUT == 2 ]]; then echo "Something unexpected happend"; fi
        echo "FAILED = $FAILED at $basename"
        if [[ $FAILED != 0 ]]; then echo "Wait 1s before retrying"; sleep 1; fi
    done
    #echo "COPY $lines RECORDS INTO $basename FROM '/tmp/$i' ON CLIENT DELIMITERS '|' NULL AS '';" >> load.sql
done

######################## End measurement of time ########################
bexhoma_end_epoch=$(date -u +%s)
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show timing information ###################
echo "Loading done"

DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"

SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
echo "Duration $DURATION_SCRIPT seconds (script total)"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Exit successfully ###################
# while true; do sleep 2; done
exit 0
