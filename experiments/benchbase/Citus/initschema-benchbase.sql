-- public.customer definition

-- Drop table

-- DROP TABLE public.customer;

CREATE TABLE public.customer (
	c_since timestamptz NOT NULL,
	c_id int4 NOT NULL,
	c_w_id int4 NOT NULL,
	c_d_id int2 NOT NULL,
	c_payment_cnt int2 NOT NULL,
	c_delivery_cnt int2 NOT NULL,
	c_first varchar(16) NOT NULL,
	c_middle bpchar(2) NOT NULL,
	c_last varchar(16) NOT NULL,
	c_street_1 varchar(20) NOT NULL,
	c_street_2 varchar(20) NOT NULL,
	c_city varchar(20) NOT NULL,
	c_state bpchar(2) NOT NULL,
	c_zip bpchar(9) NOT NULL,
	c_phone bpchar(16) NOT NULL,
	c_credit bpchar(2) NOT NULL,
	c_credit_lim numeric(12, 2) NOT NULL,
	c_discount numeric(4, 4) NOT NULL,
	c_balance numeric(12, 2) NOT NULL,
	c_ytd_payment numeric(12, 2) NOT NULL,
	c_data varchar(500) NOT NULL,
	CONSTRAINT customer_i1 PRIMARY KEY (c_w_id, c_d_id, c_id)
);
CREATE UNIQUE INDEX customer_i2 ON public.customer USING btree (c_w_id, c_d_id, c_last, c_first, c_id);


-- public.district definition

-- Drop table

-- DROP TABLE public.district;

CREATE TABLE public.district (
	d_w_id int4 NOT NULL,
	d_next_o_id int4 NOT NULL,
	d_id int2 NOT NULL,
	d_ytd numeric(12, 2) NOT NULL,
	d_tax numeric(4, 4) NOT NULL,
	d_name varchar(10) NOT NULL,
	d_street_1 varchar(20) NOT NULL,
	d_street_2 varchar(20) NOT NULL,
	d_city varchar(20) NOT NULL,
	d_state bpchar(2) NOT NULL,
	d_zip bpchar(9) NOT NULL,
	CONSTRAINT district_i1 PRIMARY KEY (d_w_id, d_id)
);


-- public.history definition

-- Drop table

-- DROP TABLE public.history;

CREATE TABLE public.history (
	h_date timestamptz NOT NULL,
	h_c_id int4 NULL,
	h_c_w_id int4 NOT NULL,
	h_w_id int4 NOT NULL,
	h_c_d_id int2 NOT NULL,
	h_d_id int2 NOT NULL,
	h_amount numeric(6, 2) NOT NULL,
	h_data varchar(24) NOT NULL
);


-- public.item definition

-- Drop table

-- DROP TABLE public.item;

CREATE TABLE public.item (
	i_id int4 NOT NULL,
	i_im_id int4 NOT NULL,
	i_name varchar(24) NOT NULL,
	i_price numeric(5, 2) NOT NULL,
	i_data varchar(50) NOT NULL,
	CONSTRAINT item_i1 PRIMARY KEY (i_id)
);


-- public.new_order definition

-- Drop table

-- DROP TABLE public.new_order;

CREATE TABLE public.new_order (
	no_w_id int4 NOT NULL,
	no_o_id int4 NOT NULL,
	no_d_id int2 NOT NULL,
	CONSTRAINT new_order_i1 PRIMARY KEY (no_w_id, no_d_id, no_o_id)
);


-- public.order_line definition

-- Drop table

-- DROP TABLE public.order_line;

CREATE TABLE public.order_line (
	ol_delivery_d timestamptz NULL,
	ol_o_id int4 NOT NULL,
	ol_w_id int4 NOT NULL,
	ol_i_id int4 NOT NULL,
	ol_supply_w_id int4 NOT NULL,
	ol_d_id int2 NOT NULL,
	ol_number int2 NOT NULL,
	ol_quantity int2 NOT NULL,
	ol_amount numeric(6, 2) NULL,
	ol_dist_info bpchar(24) NULL,
	CONSTRAINT order_line_i1 PRIMARY KEY (ol_w_id, ol_d_id, ol_o_id, ol_number)
);


-- public.orders definition

-- Drop table

-- DROP TABLE public.orders;

CREATE TABLE public.orders (
	o_entry_d timestamptz NOT NULL,
	o_id int4 NOT NULL,
	o_w_id int4 NOT NULL,
	o_c_id int4 NOT NULL,
	o_d_id int2 NOT NULL,
	o_carrier_id int2 NULL,
	o_ol_cnt int2 NOT NULL,
	o_all_local int2 NOT NULL,
	CONSTRAINT orders_i1 PRIMARY KEY (o_w_id, o_d_id, o_id)
);
CREATE UNIQUE INDEX orders_i2 ON public.orders USING btree (o_w_id, o_d_id, o_c_id, o_id);


-- public.stock definition

-- Drop table

-- DROP TABLE public.stock;

CREATE TABLE public.stock (
	s_i_id int4 NOT NULL,
	s_w_id int4 NOT NULL,
	s_ytd int4 NOT NULL,
	s_quantity int2 NOT NULL,
	s_order_cnt int2 NOT NULL,
	s_remote_cnt int2 NOT NULL,
	s_dist_01 bpchar(24) NOT NULL,
	s_dist_02 bpchar(24) NOT NULL,
	s_dist_03 bpchar(24) NOT NULL,
	s_dist_04 bpchar(24) NOT NULL,
	s_dist_05 bpchar(24) NOT NULL,
	s_dist_06 bpchar(24) NOT NULL,
	s_dist_07 bpchar(24) NOT NULL,
	s_dist_08 bpchar(24) NOT NULL,
	s_dist_09 bpchar(24) NOT NULL,
	s_dist_10 bpchar(24) NOT NULL,
	s_data varchar(50) NOT NULL,
	CONSTRAINT stock_i1 PRIMARY KEY (s_i_id, s_w_id)
);


-- public.warehouse definition

-- Drop table

-- DROP TABLE public.warehouse;

CREATE TABLE public.warehouse (
	w_id int4 NOT NULL,
	w_name varchar(10) NOT NULL,
	w_street_1 varchar(20) NOT NULL,
	w_street_2 varchar(20) NOT NULL,
	w_city varchar(20) NOT NULL,
	w_state bpchar(2) NOT NULL,
	w_zip bpchar(9) NOT NULL,
	w_tax numeric(4, 4) NOT NULL,
	w_ytd numeric(16, 2) NOT NULL,
	CONSTRAINT warehouse_i1 PRIMARY KEY (w_id)
);



SELECT create_distributed_table('customer', 'c_w_id');
SELECT create_distributed_table('district', 'd_w_id');
SELECT create_distributed_table('history', 'h_w_id');
SELECT create_distributed_table('warehouse', 'w_id');
SELECT create_distributed_table('stock', 's_w_id');
SELECT create_distributed_table('new_order', 'no_w_id');
SELECT create_distributed_table('orders', 'o_w_id');
SELECT create_distributed_table('order_line', 'ol_w_id');
SELECT create_reference_table('item');

SELECT create_distributed_function('dbms_random(int,int)');
SELECT create_distributed_function(oid, '$1', colocate_with:='warehouse') FROM pg_catalog.pg_proc WHERE proname IN ('neword', 'delivery', 'payment', 'ostat', 'slev');

-- Verify Distribution
SELECT * FROM citus_shards;

SELECT 'pg_stat_replication' AS message;
SELECT * FROM pg_stat_replication;

SELECT 'pg_dist_partition' AS message;
SELECT * from pg_dist_partition;

SELECT 'pg_dist_shard' AS message;
SELECT * from pg_dist_shard;

SELECT 'citus_shards' AS message;
SELECT * FROM citus_shards;

SELECT 'pg_dist_placement' AS message;
SELECT * from pg_dist_placement;

SELECT 'pg_dist_node' AS message;
SELECT * from pg_dist_node;

SELECT 'citus_tables' AS message;
SELECT * FROM citus_tables;

SELECT 'citus_get_active_worker_nodes' AS message;
SELECT * FROM citus_get_active_worker_nodes();

