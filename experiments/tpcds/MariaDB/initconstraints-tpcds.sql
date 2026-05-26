-- Benchmark-Experiment-Host-Manager | experiments/tpcds/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add foreign key constraints to TPC-DS tables in MariaDB.
--          Run after initschema-tpcds.sql and before initindexes-tpcds.sql.

-- Legal Notice
--
-- This document and associated source code (the "Work") is a part of a
-- benchmark specification maintained by the TPC.
--
-- The TPC reserves all right, title, and interest to the Work as provided
-- under U.S. and international laws, including without limitation all patent
-- and trademark rights therein.
--
-- No Warranty
--
-- 1.1 TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE INFORMATION
--     CONTAINED HEREIN IS PROVIDED "AS IS" AND WITH ALL FAULTS, AND THE
--     AUTHORS AND DEVELOPERS OF THE WORK HEREBY DISCLAIM ALL OTHER
--     WARRANTIES AND CONDITIONS, EITHER EXPRESS, IMPLIED OR STATUTORY,
--     INCLUDING, BUT NOT LIMITED TO, ANY (IF ANY) IMPLIED WARRANTIES,
--     DUTIES OR CONDITIONS OF MERCHANTABILITY, OF FITNESS FOR A PARTICULAR
--     PURPOSE, OF ACCURACY OR COMPLETENESS OF RESPONSES, OF RESULTS, OF
--     WORKMANLIKE EFFORT, OF LACK OF VIRUSES, AND OF LACK OF NEGLIGENCE.
--     ALSO, THERE IS NO WARRANTY OR CONDITION OF TITLE, QUIET ENJOYMENT,
--     QUIET POSSESSION, CORRESPONDENCE TO DESCRIPTION OR NON-INFRINGEMENT
--     WITH REGARD TO THE WORK.
-- 1.2 IN NO EVENT WILL ANY AUTHOR OR DEVELOPER OF THE WORK BE LIABLE TO
--     ANY OTHER PARTY FOR ANY DAMAGES, INCLUDING BUT NOT LIMITED TO THE
--     COST OF PROCURING SUBSTITUTE GOODS OR SERVICES, LOST PROFITS, LOSS
--     OF USE, LOSS OF DATA, OR ANY INCIDENTAL, CONSEQUENTIAL, DIRECT,
--     INDIRECT, OR SPECIAL DAMAGES WHETHER UNDER CONTRACT, TORT, WARRANTY,
--     OR OTHERWISE, ARISING IN ANY WAY OUT OF THIS OR ANY OTHER AGREEMENT
--     RELATING TO THE WORK, WHETHER OR NOT SUCH AUTHOR OR DEVELOPER HAD
--     ADVANCE NOTICE OF THE POSSIBILITY OF SUCH DAMAGES.
--
-- Contributors:
-- Gradient Systems

ALTER TABLE tpcds.household_demographics
    ADD CONSTRAINT hd_ib FOREIGN KEY (hd_income_band_sk) REFERENCES tpcds.income_band (ib_income_band_sk);

ALTER TABLE tpcds.call_center
    ADD CONSTRAINT cc_d1 FOREIGN KEY (cc_closed_date_sk) REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT cc_d2 FOREIGN KEY (cc_open_date_sk)   REFERENCES tpcds.date_dim (d_date_sk);

ALTER TABLE tpcds.catalog_page
    ADD CONSTRAINT cp_d1 FOREIGN KEY (cp_end_date_sk)   REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT cp_d2 FOREIGN KEY (cp_start_date_sk) REFERENCES tpcds.date_dim (d_date_sk);
-- catalog_page→promotion FK not applied: column cp_promo_id does not exist in catalog_page

ALTER TABLE tpcds.store
    ADD CONSTRAINT s_close_date FOREIGN KEY (s_closed_date_sk) REFERENCES tpcds.date_dim (d_date_sk);

ALTER TABLE tpcds.web_site
    ADD CONSTRAINT web_d1 FOREIGN KEY (web_close_date_sk) REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT web_d2 FOREIGN KEY (web_open_date_sk)  REFERENCES tpcds.date_dim (d_date_sk);

ALTER TABLE tpcds.web_page
    ADD CONSTRAINT wp_ad FOREIGN KEY (wp_access_date_sk)   REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT wp_cd FOREIGN KEY (wp_creation_date_sk) REFERENCES tpcds.date_dim (d_date_sk);

ALTER TABLE tpcds.promotion
    ADD CONSTRAINT p_end_date   FOREIGN KEY (p_end_date_sk)   REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT p_i          FOREIGN KEY (p_item_sk)       REFERENCES tpcds.item (i_item_sk),
    ADD CONSTRAINT p_start_date FOREIGN KEY (p_start_date_sk) REFERENCES tpcds.date_dim (d_date_sk);

ALTER TABLE tpcds.customer
    ADD CONSTRAINT c_a    FOREIGN KEY (c_current_addr_sk)      REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT c_cd   FOREIGN KEY (c_current_cdemo_sk)     REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT c_hd   FOREIGN KEY (c_current_hdemo_sk)     REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT c_fsd  FOREIGN KEY (c_first_sales_date_sk)  REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT c_fsd2 FOREIGN KEY (c_first_shipto_date_sk) REFERENCES tpcds.date_dim (d_date_sk);

ALTER TABLE tpcds.inventory
    ADD CONSTRAINT inv_d FOREIGN KEY (inv_date_sk)      REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT inv_i FOREIGN KEY (inv_item_sk)      REFERENCES tpcds.item (i_item_sk),
    ADD CONSTRAINT inv_w FOREIGN KEY (inv_warehouse_sk) REFERENCES tpcds.warehouse (w_warehouse_sk);

ALTER TABLE tpcds.store_returns
    ADD CONSTRAINT sr_a     FOREIGN KEY (sr_addr_sk)          REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT sr_cd    FOREIGN KEY (sr_cdemo_sk)         REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT sr_c     FOREIGN KEY (sr_customer_sk)      REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT sr_hd    FOREIGN KEY (sr_hdemo_sk)         REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT sr_i     FOREIGN KEY (sr_item_sk)          REFERENCES tpcds.item (i_item_sk),
    ADD CONSTRAINT sr_r     FOREIGN KEY (sr_reason_sk)        REFERENCES tpcds.reason (r_reason_sk),
    ADD CONSTRAINT sr_ret_d FOREIGN KEY (sr_returned_date_sk) REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT sr_t     FOREIGN KEY (sr_return_time_sk)   REFERENCES tpcds.time_dim (t_time_sk),
    ADD CONSTRAINT sr_s     FOREIGN KEY (sr_store_sk)         REFERENCES tpcds.store (s_store_sk);

ALTER TABLE tpcds.catalog_returns
    ADD CONSTRAINT cr_cc  FOREIGN KEY (cr_call_center_sk)        REFERENCES tpcds.call_center (cc_call_center_sk),
    ADD CONSTRAINT cr_cp  FOREIGN KEY (cr_catalog_page_sk)       REFERENCES tpcds.catalog_page (cp_catalog_page_sk),
    ADD CONSTRAINT cr_i   FOREIGN KEY (cr_item_sk)               REFERENCES tpcds.item (i_item_sk),
    ADD CONSTRAINT cr_r   FOREIGN KEY (cr_reason_sk)             REFERENCES tpcds.reason (r_reason_sk),
    ADD CONSTRAINT cr_a1  FOREIGN KEY (cr_refunded_addr_sk)      REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT cr_cd1 FOREIGN KEY (cr_refunded_cdemo_sk)     REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT cr_c1  FOREIGN KEY (cr_refunded_customer_sk)  REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT cr_hd1 FOREIGN KEY (cr_refunded_hdemo_sk)     REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT cr_d1  FOREIGN KEY (cr_returned_date_sk)      REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT cr_t   FOREIGN KEY (cr_returned_time_sk)      REFERENCES tpcds.time_dim (t_time_sk),
    ADD CONSTRAINT cr_a2  FOREIGN KEY (cr_returning_addr_sk)     REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT cr_cd2 FOREIGN KEY (cr_returning_cdemo_sk)    REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT cr_c2  FOREIGN KEY (cr_returning_customer_sk) REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT cr_hd2 FOREIGN KEY (cr_returning_hdemo_sk)    REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT cr_sm  FOREIGN KEY (cr_ship_mode_sk)          REFERENCES tpcds.ship_mode (sm_ship_mode_sk),
    ADD CONSTRAINT cr_w2  FOREIGN KEY (cr_warehouse_sk)          REFERENCES tpcds.warehouse (w_warehouse_sk);
-- catalog_returns→date_dim (cr_ship_date_sk) FK not applied: cr_ship_date_sk intentionally omitted per TPC-DS specification

ALTER TABLE tpcds.web_returns
    ADD CONSTRAINT wr_i      FOREIGN KEY (wr_item_sk)               REFERENCES tpcds.item (i_item_sk),
    ADD CONSTRAINT wr_r      FOREIGN KEY (wr_reason_sk)             REFERENCES tpcds.reason (r_reason_sk),
    ADD CONSTRAINT wr_ref_a  FOREIGN KEY (wr_refunded_addr_sk)      REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT wr_ref_cd FOREIGN KEY (wr_refunded_cdemo_sk)     REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT wr_ref_c  FOREIGN KEY (wr_refunded_customer_sk)  REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT wr_ref_hd FOREIGN KEY (wr_refunded_hdemo_sk)     REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT wr_ret_d  FOREIGN KEY (wr_returned_date_sk)      REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT wr_ret_t  FOREIGN KEY (wr_returned_time_sk)      REFERENCES tpcds.time_dim (t_time_sk),
    ADD CONSTRAINT wr_ret_a  FOREIGN KEY (wr_returning_addr_sk)     REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT wr_ret_cd FOREIGN KEY (wr_returning_cdemo_sk)    REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT wr_ret_c  FOREIGN KEY (wr_returning_customer_sk) REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT wr_ret_hd FOREIGN KEY (wr_returning_hdemo_sk)    REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT wr_wp     FOREIGN KEY (wr_web_page_sk)           REFERENCES tpcds.web_page (wp_web_page_sk);

ALTER TABLE tpcds.catalog_sales
    ADD CONSTRAINT cs_b_a  FOREIGN KEY (cs_bill_addr_sk)      REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT cs_b_cd FOREIGN KEY (cs_bill_cdemo_sk)     REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT cs_b_c  FOREIGN KEY (cs_bill_customer_sk)  REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT cs_b_hd FOREIGN KEY (cs_bill_hdemo_sk)     REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT cs_cc   FOREIGN KEY (cs_call_center_sk)    REFERENCES tpcds.call_center (cc_call_center_sk),
    ADD CONSTRAINT cs_cp   FOREIGN KEY (cs_catalog_page_sk)   REFERENCES tpcds.catalog_page (cp_catalog_page_sk),
    ADD CONSTRAINT cs_i    FOREIGN KEY (cs_item_sk)           REFERENCES tpcds.item (i_item_sk),
    ADD CONSTRAINT cs_p    FOREIGN KEY (cs_promo_sk)          REFERENCES tpcds.promotion (p_promo_sk),
    ADD CONSTRAINT cs_s_a  FOREIGN KEY (cs_ship_addr_sk)      REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT cs_s_cd FOREIGN KEY (cs_ship_cdemo_sk)     REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT cs_s_c  FOREIGN KEY (cs_ship_customer_sk)  REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT cs_d1   FOREIGN KEY (cs_ship_date_sk)      REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT cs_s_hd FOREIGN KEY (cs_ship_hdemo_sk)     REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT cs_sm   FOREIGN KEY (cs_ship_mode_sk)      REFERENCES tpcds.ship_mode (sm_ship_mode_sk),
    ADD CONSTRAINT cs_d2   FOREIGN KEY (cs_sold_date_sk)      REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT cs_t    FOREIGN KEY (cs_sold_time_sk)      REFERENCES tpcds.time_dim (t_time_sk),
    ADD CONSTRAINT cs_w    FOREIGN KEY (cs_warehouse_sk)      REFERENCES tpcds.warehouse (w_warehouse_sk);

ALTER TABLE tpcds.store_sales
    ADD CONSTRAINT ss_a  FOREIGN KEY (ss_addr_sk)      REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT ss_cd FOREIGN KEY (ss_cdemo_sk)     REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT ss_c  FOREIGN KEY (ss_customer_sk)  REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT ss_hd FOREIGN KEY (ss_hdemo_sk)     REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT ss_i  FOREIGN KEY (ss_item_sk)      REFERENCES tpcds.item (i_item_sk),
    ADD CONSTRAINT ss_p  FOREIGN KEY (ss_promo_sk)     REFERENCES tpcds.promotion (p_promo_sk),
    ADD CONSTRAINT ss_d  FOREIGN KEY (ss_sold_date_sk) REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT ss_t  FOREIGN KEY (ss_sold_time_sk) REFERENCES tpcds.time_dim (t_time_sk),
    ADD CONSTRAINT ss_s  FOREIGN KEY (ss_store_sk)     REFERENCES tpcds.store (s_store_sk);

ALTER TABLE tpcds.web_sales
    ADD CONSTRAINT ws_b_a  FOREIGN KEY (ws_bill_addr_sk)      REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT ws_b_cd FOREIGN KEY (ws_bill_cdemo_sk)     REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT ws_b_c  FOREIGN KEY (ws_bill_customer_sk)  REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT ws_b_hd FOREIGN KEY (ws_bill_hdemo_sk)     REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT ws_i    FOREIGN KEY (ws_item_sk)           REFERENCES tpcds.item (i_item_sk),
    ADD CONSTRAINT ws_p    FOREIGN KEY (ws_promo_sk)          REFERENCES tpcds.promotion (p_promo_sk),
    ADD CONSTRAINT ws_s_a  FOREIGN KEY (ws_ship_addr_sk)      REFERENCES tpcds.customer_address (ca_address_sk),
    ADD CONSTRAINT ws_s_cd FOREIGN KEY (ws_ship_cdemo_sk)     REFERENCES tpcds.customer_demographics (cd_demo_sk),
    ADD CONSTRAINT ws_s_c  FOREIGN KEY (ws_ship_customer_sk)  REFERENCES tpcds.customer (c_customer_sk),
    ADD CONSTRAINT ws_s_d  FOREIGN KEY (ws_ship_date_sk)      REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT ws_s_hd FOREIGN KEY (ws_ship_hdemo_sk)     REFERENCES tpcds.household_demographics (hd_demo_sk),
    ADD CONSTRAINT ws_sm   FOREIGN KEY (ws_ship_mode_sk)      REFERENCES tpcds.ship_mode (sm_ship_mode_sk),
    ADD CONSTRAINT ws_d2   FOREIGN KEY (ws_sold_date_sk)      REFERENCES tpcds.date_dim (d_date_sk),
    ADD CONSTRAINT ws_t    FOREIGN KEY (ws_sold_time_sk)      REFERENCES tpcds.time_dim (t_time_sk),
    ADD CONSTRAINT ws_w2   FOREIGN KEY (ws_warehouse_sk)      REFERENCES tpcds.warehouse (w_warehouse_sk),
    ADD CONSTRAINT ws_wp   FOREIGN KEY (ws_web_page_sk)       REFERENCES tpcds.web_page (wp_web_page_sk),
    ADD CONSTRAINT ws_ws   FOREIGN KEY (ws_web_site_sk)       REFERENCES tpcds.web_site (web_site_sk);
